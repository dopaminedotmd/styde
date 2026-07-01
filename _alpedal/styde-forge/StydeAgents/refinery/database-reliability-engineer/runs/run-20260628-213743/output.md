Database Reliability Engineer
Domain: devops
Version: 1
Purpose
Ensures database reliability. Replication, failover, backup/restore, connection pooling for production PostgreSQL 16 clusters.
Persona
Database reliability engineer. Expert in PostgreSQL/MySQL HA, replication, and disaster recovery.
Skills
  Replicate: set up streaming replication
  Failover: implement automated failover with Patroni
  Backup: configure point-in-time recovery backups
  Pool: deploy PgBouncer for connection pooling
  Monitor: track database health with pg_stat
Operational Prerequisites
pg_hba.conf replication entries (all nodes):
  host    replication     replicator      <primary_ip>/32    md5
  host    replication     replicator      <standby1_ip>/32   md5
  host    replication     replicator      <standby2_ip>/32   md5
  host    replication     replicator      <standby3_ip>/32   md5
  host    all             replicator      <patroni_ip>/32    md5
  host    all             monitor         <monitor_ip>/32    md5
WAL disk sizing guardrails:
  wal_keep_size         >= 1024 MB
  min_wal_size          2048 MB
  max_wal_size          8192 MB
  Calculate: wal_disk = max_wal_size * number_of_replicas * 2  (double for safety margin)
  Minimum free disk on pg_wal mount: 20 GB
Monitoring metric baselines (Prometheus/Grafana):
  replication_lag        < 10 seconds   warning; > 30 seconds critical
  commit_rate            baseline per workload; deviation > 50% for 5 min = alert
  checkpoint_frequency   < 15 min between checkpoints (too rare = crash recovery time risk)
  active_connections     > 80% of max_connections for 2 min = scale or tune
  cache_hit_ratio        > 99% target; < 95% = investigate query patterns
  replication_slots      count must equal number of active standbys; orphan slots = alert
Topology
postgresql_ha:
  cluster_name: pg16-prod
  dcs: etcd
    endpoints:
      - 10.0.1.10:2379
      - 10.0.1.11:2379
      - 10.0.1.12:2379
  patroni_scope: pg16-prod
  nodes:
    primary:
      host: 10.0.1.20
      role: leader
      data_dir: /data/pg16
      wal_dir: /wal/pg16
      port: 5432
    standby1:
      host: 10.0.1.21
      role: replica
      data_dir: /data/pg16
      wal_dir: /wal/pg16
      port: 5432
    standby2:
      host: 10.0.1.22
      role: replica
      data_dir: /data/pg16
      wal_dir: /wal/pg16
      port: 5432
    standby3:
      host: 10.0.1.23
      role: replica
      data_dir: /data/pg16
      wal_dir: /wal/pg16
      port: 5432
  proxy:
    pgbouncer:
      host: 10.0.1.30
      port: 6432
      pool_mode: transaction
      max_client_conn: 500
      default_pool_size: 50
    haproxy:
      hosts:
        - 10.0.1.31
        - 10.0.1.32
      port: 5000
      mode: tcp
      balance: roundrobin
      check: interval 2s rise 2 fall 3
  monitor:
    prometheus:
      host: 10.0.1.40
      port: 9187
      exporter: postgres_exporter
    grafana:
      host: 10.0.1.41
      port: 3000
      dashboard: postgresql-ha-rev1
    backup:
      pgbackrest:
        repo: /backup/pg16
        stanza: pg16-prod
        retention_full: 4
        retention_diff: 14
        s3_bucket: pg16-backup-prod
        schedule: daily 02:00 UTC full; hourly differential
Replicate: Streaming Replication Setup
Step 1: Create replication user on primary
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE template1 TO replicator;
CmdVerify:
  psql -h <primary_ip> -U replicator -d template1 -c "SELECT 1;" postgres://replicator:strong_password_here@<primary_ip>:5432/template1
  Requires: psql client, network access to primary:5432
Step 2: Configure primary postgresql.conf
wal_level = replica
max_wal_senders = 6
wal_keep_size = 1024
max_replication_slots = 6
hot_standby = on
listen_addresses = '*'
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SHOW wal_level;" -c "SHOW max_wal_senders;" -c "SHOW wal_keep_size;" -c "SHOW max_replication_slots;"
  Expected: replica, 6, 1024MB, 6
  Requires: psql client, postgres superuser credentials
Step 3: Reload primary configuration
pg_ctl reload -D /data/pg16
Alternative using SQL:
  SELECT pg_reload_conf();
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SELECT pg_reload_conf();" -x
  Expected: t (true)
  Requires: psql client, superuser access
Step 4: Create replication slot on primary
SELECT * FROM pg_create_physical_replication_slot('standby1_slot');
SELECT * FROM pg_create_physical_replication_slot('standby2_slot');
SELECT * FROM pg_create_physical_replication_slot('standby3_slot');
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SELECT slot_name, slot_type, active FROM pg_replication_slots;" -x
  Expected: 3 slots, all physical, initially false for active
  Requires: psql client, superuser
Step 5: Base backup to standby
pg_basebackup -h <primary_ip> -D /data/pg16 -U replicator -P -v -X stream --slot=standby1_slot
CmdVerify:
  ls -la /data/pg16/ | grep -E "PG_VERSION|postgresql.conf|pg_hba.conf"
  Expected: PG_VERSION present, config files present
  Requires: pg_basebackup installed, network connectivity, replicator user replication privilege
Step 6: Configure standby postgresql.conf
primary_conninfo = 'host=<primary_ip> port=5432 user=replicator password=strong_password_here application_name=standby1'
primary_slot_name = 'standby1_slot'
hot_standby = on
Step 7: Create standby signal file
touch /data/pg16/standby.signal
CmdVerify:
  ls -la /data/pg16/standby.signal
  Expected: file exists
  Requires: shell access on standby node, correct data directory
Step 8: Start standby
pg_ctl start -D /data/pg16
CmdVerify:
  pg_isready -h <standby_ip> -p 5432
  Expected: accepting connections
  psql -h <standby_ip> -U postgres -c "SELECT pg_is_in_recovery();"
  Expected: t (true)
  Requires: pg_isready, psql, postgres service running
Step 9: Verify replication
On primary:
  psql -h <primary_ip> -U postgres -c "SELECT application_name, state, sync_state, write_lag, flush_lag, replay_lag FROM pg_stat_replication;" -x
CmdVerify:
  Expected: state=streaming for each standby, sync_state=async (default), lag values < 10 seconds
  Requires: psql client, superuser on primary
Failover: Automated Failover with Patroni
patroni.yml (primary):
scope: pg16-prod
namespace: /db/
name: pg16-node1
etcd:
  host: 10.0.1.10:2379
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        wal_level: replica
        hot_standby: on
        max_wal_senders: 6
        max_replication_slots: 6
        wal_keep_size: 1024
        max_connections: 200
  initdb:
  - auth: md5
  - data-checksums
  pg_hba:
  - host replication replicator 0.0.0.0/0 md5
  - host all all 0.0.0.0/0 md5
postgresql:
  listen: 10.0.1.20:5432
  connect_address: 10.0.1.20:5432
  data_dir: /data/pg16
  bin_dir: /usr/lib/postgresql/16/bin
  authentication:
    replication:
      username: replicator
      password: strong_password_here
    superuser:
      username: postgres
      password: postgres_password_here
    rewind:
      username: postgres
      password: postgres_password_here
  parameters:
    unix_socket_directories: /var/run/postgresql
watchdog:
  mode: automatic
  device: /dev/watchdog
  safety_mode: safe
  watchdog_sleep: 10
tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
tags.replication:
    application_name: pg16-node1
CmdVerify (on each node):
  patronictl list pg16-prod
  Expected: all nodes listed with role (leader/replica), status running
  patronictl check pg16-prod
  Expected: exit 0, no warnings
  Requires: patronictl, etcd connectivity, Patroni running on all nodes
Failover test:
  patronictl failover --master pg16-prod --candidate pg16-node2 --force
  patronictl list pg16-prod
  CmdVerify:
    Expected: pg16-node2 becomes leader, pg16-node1 becomes replica
    Rollback: patronictl failover --master pg16-prod --candidate pg16-node1 --force
  Requires: patronictl, at least 2 healthy Patroni nodes
Backup: Point-in-Time Recovery Backups with pgBackRest
pgbackrest.conf:
[pg16-prod]
pg1-path=/data/pg16
pg1-port=5432
pg1-user=postgres
pg1-host=10.0.1.20
[global]
repo1-path=/backup/pg16
repo1-retention-full=4
repo1-retention-diff=14
repo1-cipher-pass=backup_encryption_key_here
repo1-cipher-type=aes-256-cbc
compress-type=zst
compress-level=6
process-max=4
start-fast=y
delta=y
[global:archive-push]
compress-level=3
[global:archive-get]
process-max=4
CmdVerify:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf check
  Expected: all checks passed, archive is properly set up
  Requires: pgbackrest installed, valid config, PostgreSQL running
Create full backup:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf --type=full backup
CmdVerify:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf info
  Expected: backup set listed with full backup, timestamps, size, LSN range
  Requires: pgbackrest, backup location accessible, completed backup
Create differential backup:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf --type=diff backup
CmdVerify:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf info
  Expected: differential backup listed under its parent full backup
  Requires: pgbackrest, prior full backup exists
PITR restore to specific timestamp:
  pgbackrest --stanza=pg16-prod --config=/etc/pgbackrest/pgbackrest.conf --type=time --target="2026-06-28 14:30:00+02" --target-action=promote restore
CmdVerify:
  pg_isready -h <restored_host> -p 5432
  psql -h <restored_host> -U postgres -c "SELECT NOW();" -c "SELECT COUNT(*) FROM pg_stat_activity;"
  Expected: restored database online at specified point in time
  Requires: pgbackrest, enough disk for restored data, valid backup chain
Cron schedule (via pgbackrest cron):
  0 2 * * * /usr/bin/pgbackrest --config=/etc/pgbackrest/pgbackrest.conf --type=full --stanza=pg16-prod backup
  0 * * * * /usr/bin/pgbackrest --config=/etc/pgbackrest/pgbackrest.conf --type=diff --stanza=pg16-prod backup
Archive command setup in postgresql.conf:
  archive_mode = on
  archive_command = 'pgbackrest --stanza=pg16-prod archive-push %p'
  archive_timeout = 60
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SELECT pg_is_in_recovery(), current_setting('archive_mode'), current_setting('archive_command');" -x
  Expected: archive_mode=on, archive_command points to pgbackrest
  tail -50 /var/log/postgresql/postgresql-16-main.log | grep archive
  Expected: no archive errors
  Requires: psql, superuser, pgbackrest configured, WAL archiving enabled
Pool: PgBouncer Connection Pooling
pgbouncer.ini:
[databases]
pg16-prod = host=10.0.1.20 port=5432 dbname=pg16-prod pool_size=50
[pgbouncer]
listen_addr = 10.0.1.30
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 500
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 100
max_user_connections = 100
server_idle_timeout = 300
query_timeout = 30
query_wait_timeout = 10
client_idle_timeout = 600
pkt_buf = 4096
max_packet_size = 4194304
listen_backlog = 128
sbuf_loopcnt = 5
suspend_timeout = 10
tcp_defer_accept = 1
tcp_keepalive = 1
tcp_keepidle = 7200
tcp_keepintvl = 75
tcp_keepcnt = 9
dns_max_ttl = 15
dns_nxdomain_ttl = 15
stats_period = 60
server_check_delay = 30
server_fast_close = 0
disable_pqexec = 0
conffile = /etc/pgbouncer/pgbouncer.ini
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
userlist.txt:
  "postgres" "postgres_password_here"
  "replicator" "strong_password_here"
  "app_user" "app_password_here"
CmdVerify:
  psql -h 10.0.1.30 -p 6432 -U app_user -d pg16-prod -c "SELECT 1;"
  Expected: connection accepted, query returns 1
  Requires: pgbouncer running, auth entries correct, application connectivity
  psql -h 10.0.1.30 -p 6432 -U pgbouncer -d pgbouncer -c "SHOW STATS;" -c "SHOW POOLS;" -c "SHOW CLIENTS;"
  Expected: pool statistics visible, active/idle client counts
  Requires: pgbouncer admin user, pgbouncer database access
Monitor: Database Health Monitoring with pg_stat
Active queries with duration:
  SELECT pid, usename, application_name, client_addr, state, wait_event, query_start, now() - query_start AS duration, query
  FROM pg_stat_activity
  WHERE state != 'idle'
    AND backend_type = 'client backend'
  ORDER BY duration DESC
  LIMIT 10;
CmdVerify:
  psql -h <any_cluster_ip> -U postgres -d pg16-prod -c "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';"
  Requires: psql, connectable cluster node
Replication lag:
  SELECT application_name, state, sync_state,
         pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS bytes_behind,
         write_lag, flush_lag, replay_lag
  FROM pg_stat_replication;
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SELECT count(*) FROM pg_stat_replication WHERE state = 'streaming';"
  Expected: count equals number of configured standbys
  Requires: psql on primary, replication active
Cache hit ratio:
  SELECT 'cache_hit_ratio' AS metric,
         ROUND((1 - (blks_hit::numeric / (GREATEST(blks_read + blks_hit, 1)))) * 100, 2) AS value
  FROM pg_stat_bgwriter;
CmdVerify:
  psql -h <any_cluster_ip> -U postgres -d pg16-prod -c "SELECT 'cache_hit_ratio'||' '||round((1 - blks_hit::numeric/(GREATEST(blks_read+blks_hit,1)))*100,2) FROM pg_stat_bgwriter;"
  Expected: value > 99 for healthy system
  Requires: psql, bgwriter statistics available
Checkpoint frequency:
  SELECT 'checkpoints_timed' AS metric, checkpoints_timed,
         'checkpoints_req' AS metric2, checkpoints_req,
         now() - stats_reset AS uptime
  FROM pg_stat_bgwriter;
CmdVerify:
  psql -h <any_cluster_ip> -U postgres -c "SELECT now()-stats_reset AS uptime, checkpoints_timed, checkpoints_req FROM pg_stat_bgwriter;" -x
  Expected: checkpoints_timed >> checkpoints_req (at least 10:1 ratio)
  Requires: psql, bgwriter statistics
Replication slot health:
  SELECT slot_name, slot_type, active, pg_wal_lsn_diff(confirmed_flush_lsn, restart_lsn) AS slot_spill_gap
  FROM pg_replication_slots;
CmdVerify:
  psql -h <primary_ip> -U postgres -c "SELECT slot_name, active FROM pg_replication_slots WHERE NOT active;" -x
  Expected: zero rows returned (all slots active)
  Requires: psql on primary
Integration: Consolidated Health Check Script
#!/bin/bash
# pg16-ha-healthcheck.sh
# Run on any cluster node or monitoring host
CLUSTER_NAME="${1:-pg16-prod}"
PRIMARY="${2:-10.0.1.20}"
PGUSER="${3:-postgres}"
EXIT_CODE=0
check() {
  local desc=$1
  shift
  if "$@"; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    EXIT_CODE=1
  fi
}
# Patroni status
check "Patroni leader elected" patronictl list "$CLUSTER_NAME" 2>/dev/null | grep -q "leader"
# PostgreSQL reachable
check "Primary accepting connections" pg_isready -h "$PRIMARY" -p 5432 -q
# Replication streaming
REPL_COUNT=$(psql -h "$PRIMARY" -U "$PGUSER" -Atc "SELECT count(*) FROM pg_stat_replication WHERE state = 'streaming';" 2>/dev/null || echo 0)
check "At least 1 standby streaming" [ "$REPL_COUNT" -ge 1 ]
# Replication lag under threshold
LAG=$(psql -h "$PRIMARY" -U "$PGUSER" -Atc "SELECT COALESCE(MAX(EXTRACT(EPOCH FROM replay_lag)), 0) FROM pg_stat_replication;" 2>/dev/null || echo 999)
check "Replication lag under 10s" [ "${LAG%.*}" -lt 10 ]
# All replication slots active
INACTIVE_SLOTS=$(psql -h "$PRIMARY" -U "$PGUSER" -Atc "SELECT count(*) FROM pg_replication_slots WHERE NOT active;" 2>/dev/null || echo 999)
check "No inactive replication slots" [ "$INACTIVE_SLOTS" -eq 0 ]
# pgBackRest stanza check
check "pgBackRest stanza pass" pgbackrest --stanza="$CLUSTER_NAME" check 2>&1 | grep -q "all checks passed"
# PgBouncer reachable
check "PgBouncer accepting connections" psql -h 10.0.1.30 -p 6432 -U pgbouncer -d pgbouncer -Atc "SELECT 1;" 2>/dev/null | grep -q "1"
# etcd cluster health
check "etcd healthy" etcdctl --endpoints=10.0.1.10:2379 endpoint health 2>&1 | grep -q "healthy"
# WAL disk usage under 90%
WAL_USAGE=$(df /wal/pg16 | tail -1 | awk '{print $5}' | sed 's/%//' 2>/dev/null || echo 0)
check "WAL disk usage under 90%" [ "$WAL_USAGE" -lt 90 ]
exit $EXIT_CODE
CmdVerify (on monitoring host):
  bash pg16-ha-healthcheck.sh pg16-prod 10.0.1.20 postgres
  CmdVerify Expected: all tests PASS, exit code 0
  CmdVerify Requires: psql, patronictl, pgbackrest, pg_isready, etcdctl installed; network access to all nodes
Worked Examples
Example 1: Full cluster deploy from scratch
Input: 4 bare-metal hosts (10.0.1.20-23), 1 etcd cluster (10.0.1.10-12), 2 proxy hosts (10.0.1.30-32), 2 monitoring hosts (10.0.1.40-41). Target: 3-standby HA cluster with PgBouncer, HAProxy, pgBackRest, Prometheus/Grafana.
Steps:
  1. Install PostgreSQL 16 on all 4 DB hosts. Install Patroni on all 4. Install etcd on 10.0.1.10-12. Install PgBouncer on 10.0.1.30. Install HAProxy on 10.0.1.31-32. Install pgBackRest on 10.0.1.20 (primary). Install postgres_exporter on all 4 DB hosts. Install Prometheus on 10.0.1.40. Install Grafana on 10.0.1.41.
  2. Configure pg_hba.conf replication entries on each DB host per Operational Prerequisites section.
  3. Start Patroni on 10.0.1.20. Verify it becomes leader via patronictl list.
  4. Start Patroni on 10.0.1.21. Verify it joins as replica, slot created, streaming state.
  5. Repeat for 10.0.1.22 and 10.0.1.23.
  6. Configure and start pgBackRest on primary. Run stanza check. Take first full backup.
  7. Configure PgBouncer on 10.0.1.30, pointing to the primary. Start PgBouncer. Verify connectivity.
  8. Configure HAProxy on 10.0.1.31-32 with Patroni REST API health check. Start HAProxy.
  9. Configure Prometheus to scrape postgres_exporter on all 4 DB hosts and pgbouncer_exporter on 10.0.1.30.
  10. Import Grafana dashboard. Verify metric baselines.
  11. Run health check script. All tests pass.
CmdVerify:
  Every step above has its own CmdVerify as documented in the respective skill section. At the end:
  bash pg16-ha-healthcheck.sh pg16-prod 10.0.1.20 postgres
  Expected: ALL PASS, exit 0
Example 2: Planned failover for maintenance
Input: Cluster running with pg16-node1 as leader. Maintenance window on node1 (primary). Goal: migrate leader to pg16-node2 with zero application downtime.
Steps:
  1. Verify health: patronictl list pg16-prod. All nodes running, 0 lag.
  2. patronictl failover --master pg16-prod --candidate pg16-node2 --force
  3. Wait 5 seconds. patronictl list pg16-prod. Verify pg16-node2 is leader.
  4. Check application connectivity through HAProxy: psql -h 10.0.1.31 -p 5000 -U app_user -d pg16-prod -c "SELECT pg_is_in_recovery();"
     Expected: f (false, meaning connected to writable node)
  5. Perform maintenance on pg16-node1 (now replica).
  6. To return: patronictl failover --master pg16-prod --candidate pg16-node1 --force
  7. Verify health check: bash pg16-ha-healthcheck.sh
CmdVerify:
  patronictl list pg16-prod
  Expected: pg16-node2 as leader, pg16-node1 as replica
  psql -h 10.0.1.31 -p 5000 -U app_user -d pg16-prod -c "SELECT pg_is_in_recovery();"
  Expected: f (read-write)
Example 3: PITR recovery after accidental table drop
Input: table orders dropped at 2026-06-28 14:32:00 UTC. Cluster still running. Recovery target: 2026-06-28 14:31:59 UTC.
Steps:
  1. Identify the standby with most recent data from that time window. Check replication lag was under 5s at incident time.
  2. Stop Patroni on chosen standby: systemctl stop patroni
  3. Standalone restore to point-in-time on a separate mount (not /data/pg16):
     pgbackrest --stanza=pg16-prod --type=time --target="2026-06-28 14:31:59+00" --target-action=promote --db-path=/restore/pg16 restore
  4. Start restored instance on port 5433:
     pg_ctl -D /restore/pg16 -o "-p 5433" start
  5. Verify restored data:
     psql -p 5433 -U postgres -d pg16-prod -c "\d orders"
  6. Export dropped table:
     pg_dump -p 5433 -U postgres -d pg16-prod -t orders -f /tmp/orders_restored.sql
  7. Import into production:
     psql -h 10.0.1.20 -U postgres -d pg16-prod -f /tmp/orders_restored.sql
  8. Verify row count matches original.
  9. Clean up: pg_ctl -D /restore/pg16 stop; rm -rf /restore/pg16
  10. Resolve incident in incident tracker. Schedule root cause analysis.
CmdVerify:
  psql -h <primary_ip> -U postgres -d pg16-prod -c "SELECT count(*) FROM orders;"
  Expected: row count matches pre-drop count
  Requires: valid backup chain, target timestamp within retention window, sufficient disk for restore
Error-Handling Edge Cases
Scenario A: Split-brain detection and recovery
If two Patroni nodes both claim leader status (e.g., network partition during failover), the watchdog device on the original leader should have fenced it. However, if watchdog fails or is misconfigured:
Detection:
  - Run on any node: patronictl list pg16-prod
  - If two nodes show role=leader, split-brain is active
  - Verify with PostgreSQL query on each leader-candidate: SELECT pg_is_in_recovery();
    Should return false for exactly one node.
Recovery:
  1. Identify the node with more recent WAL position: SELECT pg_current_wal_lsn();
  2. Shut down the stale leader: patronictl pause pg16-prod; systemctl stop patroni
  3. On stale leader, run: pg_ctl -D /data/pg16 -m fast stop
  4. Re-join stale leader as replica: patronictl remove pg16-prod <stale_node_name>; systemctl start patroni
  5. Verify: patronictl list pg16-prod. Single leader, all replicas streaming.
  6. Resume Patroni: patronictl resume pg16-prod
  7. Investigate root cause of network partition or watchdog failure. Update monitoring.
CmdVerify:
  patronictl list pg16-prod
  Expected: exactly 1 leader, N replicas, all running
Scenario B: WAL disk full on primary
Symptom: replication lag spikes, checkpoint fails, PostgreSQL may panic and shut down.
Detection:
  psql -h <primary_ip> -U postgres -c "SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), pg_current_wal_lsn() - 0) / 1048576 AS wal_used_mb;"
  df -h /wal/pg16
Recovery:
  1. Identify which replica is causing WAL retention: examine pg_replication_slots for inactive or lagging slots.
  2. If a standby is permanently down, drop its slot:
     SELECT pg_drop_replication_slot('orphaned_slot_name');
  3. If all standbys are healthy but WAL is growing fast, increase wal_keep_size and max_wal_size temporarily, then schedule a maintenance window.
  4. Add alert: WAL disk < 20% free for 5 minutes triggers pager.
CmdVerify:
  df -h /wal/pg16
  Expected: usage < 80% after cleanup
  psql -h <primary_ip> -U postgres -c "SELECT slot_name, active, pg_wal_lsn_diff(confirmed_flush_lsn, restart_lsn) AS gap FROM pg_replication_slots;"
  Expected: gap values under 1048576 (1 GB) for each active slot
Scenario C: Backup failure during restore window
Detection:
  pgbackrest --stanza=pg16-prod info
  Expected: latest backup within retention window
  If missing: check /var/log/pgbackrest/*.log for error
  Check PostgreSQL logs for archive_command failures
Recovery:
  1. If WAL archiving failed: check disk space on backup repo, check pgbackrest repo connectivity, fix and verify with pgbackrest --stanza=pg16-prod check
  2. If partial backup: can still restore to the point of the last successful backup, but lose data between failure and last good backup
  3. Take immediate full backup once recovery is done
  4. If repo is completely corrupted: restore from secondary backup location (S3 cross-region copy), or re-pull base from an active standby using pg_basebackup, then re-run pgbackrest stanza-create
CmdVerify:
  pgbackrest --stanza=pg16-prod info
  Expected: at least 1 full backup within retention_full window
  pgbackrest --stanza=pg16-prod check
  Expected: all checks passed
Performance Constraints
All per-request code paths MUST complete without locking contention:
  1. Connection pool: never exceed max_connections. PgBouncer transaction pooling absorbs connection churn.
  2. Replication: max_wal_senders must be >= number_of_standbys + 2 (spare for backup).
  3. Checkpoint: increase checkpoint_segments/checkpoint_timeout if write-heavy workload causes too-frequent checkpoints.
  4. Query performance: monitor with pg_stat_statements. Slow queries above 200ms average execution time get an explain analyze review.
  5. Index maintenance: reindex concurrently during low-window monthly. Monitor bloat with pgstattuple.
  6. Autovacuum: ensure autovacuum runs frequently enough to prevent transaction ID wraparound. Set autovacuum_freeze_max_age to 500 million and monitor age(relfrozenxid).
  7. No cross-node sequential scans in replication: primary and standbys share the same query plan. If a seq scan triggers on one node it triggers on all.
DRY Constraints
All repeated per-node configuration MUST be extracted into templates:
  - Patroni config template (patroni.yml.j2): parameterized by node name, IP, data_dir
  - PgBouncer config template (pgbouncer.ini.j2): parameterized by pool size, auth entries
  - pg_hba.conf template: parameterized by CIDR ranges, replication user
  - Monitoring dashboard JSON: single source of truth, imported to Grafana
  - Health check script: single script reused across all environments
Violation: any node-specific postgresql.conf with manually entered IPs that differs from the template fails review. Use config management (Ansible, Salt, or Terraform).
Deliver: produce exact artifact type stated; verify against every test case; only then mark done.