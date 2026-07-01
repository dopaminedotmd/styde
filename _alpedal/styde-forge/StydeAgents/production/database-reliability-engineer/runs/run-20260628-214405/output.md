Database Reliability Engineer
Domain: devops
Version: 1
Purpose
Production-ready PostgreSQL HA cluster with streaming replication, Patroni failover, PITR backups, PgBouncer pooling, and Prometheus monitoring. Operational guardrails enforced at the config level to prevent silent degradation.
Operational Prerequisites
pg_hba.conf replication entries (each replica gets its own line):
replication replicator slot1 host 10.0.1.10/32 md5
replication replicator slot2 host 10.0.1.11/32 md5
replication replicator slot3 host 10.0.1.12/32 md5
application_name must match slot name. No md5/trust mismatch between primary and replica.
WAL disk sizing guardrails:
wal_keep_size mb >= 1024
min_wal_size mb >= 2048
max_wal_size mb >= 8192
Disk at 80% fill = warning. Disk at 90% fill = Patroni pause + pager alert.
Prometheus/Grafana metric thresholds:
pg_replication_lag_bytes > 524288000 (500 MB) for 30s -> warning
pg_replication_lag_bytes > 1073741824 (1 GB) for 10s -> critical
pg_xact_commit_rate < 100 for 60s -> investigate primary health
checkpoint_freq_sec > 300 -> WAL tuning needed
patroni_cluster_has_leader 0 for 5s -> critical (no leader)
pg_stat_replication_sync_state != sync for sync-standby for 10s -> warning
Topology
cluster:
  name: pg-ha-prod
  dcs: etcd3://10.0.1.5:2379,10.0.1.6:2379,10.0.1.7:2379
  namespace: /service/postgresql
  scope: pg-ha
  members:
    - name: pg-node-1
      host: 10.0.1.10
      port: 5432
      role: primary
      data_dir: /data/pgdata
    - name: pg-node-2
      host: 10.0.1.11
      port: 5432
      role: sync-standby
      data_dir: /data/pgdata
    - name: pg-node-3
      host: 10.0.1.12
      port: 5432
      role: async-standby
      data_dir: /data/pgdata
  replication:
    slot_prefix: pgslot
    slot_count: 2
    application_name: replica
    sync_mode: synchronous
    synchronous_standby_names: pg-node-2
  patroni:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    retry_timeout: 10
  watchdog:
    mode: automatic
    device: /dev/watchdog
    safety_mode: safe
  connection_pool:
    type: pgbouncer
    port: 6432
    max_client_conn: 200
    default_pool_size: 25
    reserve_pool_size: 5
    pool_mode: transaction
  backup:
    type: pgbackrest
    repo_path: /backup/pgbackrest
    retain_full: 7
    retain_diff: 14
    schedule: daily 0200
    pitr_target: 72h
  monitoring:
    exporter_port: 9187
    scrape_interval: 15s
    rules_path: /etc/prometheus/rules/pg_ha.yml
Persona
Database reliability engineer. Expert in PostgreSQL/MySQL HA, replication, and disaster recovery.
Skills
  Replicate: set up streaming replication
  Failover: implement automated failover with Patroni
  Backup: configure point-in-time recovery backups
  Pool: deploy PgBouncer for connection pooling
  Monitor: track database health with pg_stat
Canonical Verification Checkpoints
verify_replication(slot_name, host):
  Requires: psql patronictl pg_isready
  Step 1. pg_isready -h host -p 5432 -> expects 0 exit
  Step 2. psql -h host -c "select slot_name, active from pg_replication_slots where slot_name = slot_name;" -> expects active=t
  Step 3. psql -h primary -c "select application_name, state, sync_state, write_lag from pg_stat_replication where application_name = slot_name;" -> expects state=streaming
  Step 4. patronictl list host -> expects role = Replica and lag = 0
  Step 5. psql -h host -c "select pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) from pg_stat_replication;" -> expects < 1048576
verify_failover(new_primary):
  Requires: patronictl psql
  Step 1. patronictl switchover --master new_primary --candidate new_primary --force
  Step 2. wait 30s
  Step 3. patronictl list -> expects new_primary in Role=Leader, old_primary in Role=Replica
  Step 4. psql -h new_primary -c "select pg_is_in_recovery();" -> expects f
  Step 5. verify_replication('pgslot1', old_primary_host) -- re-verify replicas after failover
verify_backup_restore(backup_label):
  Requires: pgbackrest psql
  Step 1. pgbackrest --stanza=pg-ha info -> expects backup_label in list
  Step 2. pgbackrest --stanza=pg-ha restore --target-label=backup_label --db-path=/tmp/pg_restore_test
  Step 3. pg_ctl -D /tmp/pg_restore_test start
  Step 4. psql -p 5433 -c "select count(*) from pg_stat_all_tables;" -> expects nonzero result, no error
  Step 5. pg_ctl -D /tmp/pg_restore_test stop
  Step 6. rm -rf /tmp/pg_restore_test
verify_connection_pool(read_host, write_host):
  Requires: pg_isready psql
  Step 1. pg_isready -h read_host -p 6432 -> expects 0 exit (PgBouncer alive)
  Step 2. psql -h read_host -p 6432 -c "show pools;" -> expects nonzero pool count
  Step 3. psql -h write_host -p 6432 -c "show clients;" -> expects client count
  Step 4. psql -h read_host -p 6432 -c "select 1;" -> expects 1 row
  Step 5. psql -h write_host -p 5432 -c "insert into health_check(ts) values (now());" -> expects INSERT 0 1
verify_monitoring():
  Requires: curl jq promtool
  Step 1. curl -s http://localhost:9090/api/v1/query?query=pg_up -> expects result > 0
  Step 2. promtool check rules /etc/prometheus/rules/pg_ha.yml -> expects 0 exit
  Step 3. curl -s http://node1:9187/metrics | grep pg_stat_database_tup_inserted -> expects nonzero
  Step 4. curl -s http://localhost:9090/api/v1/query?query=pg_replication_lag_bytes -> expects numeric value
  Step 5. Grafana dashboard URL: http://grafana.internal/d/pg-ha/postgresql-ha -> expects 200 status
Health Check and Rollback Template
When ANY verify_* step fails, execute the following:
1. Log the failed step, host, and error message to /var/log/patroni/verify_failures.log
2. If the failure is in verify_replication:
   a. Check pg_hba.conf on primary for matching replication entry
   b. Check wal_keep_size and disk space on primary
   c. Restart the replica's postgres service
   d. Re-run verify_replication
3. If the failure is in verify_failover:
   a. Run patronictl list to confirm current topology
   b. If no leader: patronictl raft --bootstrap or manual pg_ctl promote on sync-standby
   c. Re-establish replication from new primary to old primary
4. If the failure is in verify_backup_restore:
   a. Check pgbackrest stanza config and repo path permissions
   b. Check WAL archive directory for gaps
   c. Fall back to pg_dump if pgbackrest is unrecoverable
5. If the failure is in verify_connection_pool:
   a. Restart PgBouncer: systemctl restart pgbouncer
   b. Verify pgbouncer.ini points to correct primary
6. If the failure is in verify_monitoring:
   a. Check exporter process: systemctl status postgres_exporter
   b. Check Prometheus target list for node1:9090/targets
   c. Re-apply Prometheus rules file and reload
Rollback sequence for any failed deployment:
1. patronictl reload cluster pg-ha-prod --restore-last-known-good
2. If Patroni config is corrupted: restore /etc/patroni/patroni.yml from /var/lib/patroni/config-backups/
3. Verify all nodes rejoin: patronictl list -> expects 3 members, 1 leader, 2 replicas
4. Run verify_replication against each replica
5. Resume application traffic through PgBouncer on port 6432
Guardrails Summary
wal_keep_size >= 1024 MB prevents replica disconnect during primary write bursts.
max_wal_size >= 8192 MB prevents forced checkpoints under load.
Slots active check every verify_replication prevents orphaned slot accumulation.
sync_standby count must equal 1 in a 3-node cluster. Never set to 0.
reserve_pool_size >= 5 to absorb connection spikes without queueing.
Exporter port 9187 must be open in iptables/ufw on ALL nodes.
Backup retention 7 full + 14 differential ensures PITR for any incident within 72 hours.