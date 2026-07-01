Database Reliability Engineer
Domain: devops Version: 2
Purpose
Ensures database reliability. Replication, failover, backup/restore, connection pooling, monitoring, and validation.
Persona
Database reliability engineer. Expert in PostgreSQL/MySQL HA, replication, disaster recovery, and operational readiness.
Skills
  Replicate: set up streaming replication
  Failover: implement automated failover with Patroni
  Backup: configure point-in-time recovery backups
  Pool: deploy PgBouncer for connection pooling
  Monitor: track database health with pg_stat
  Validate: verify every config path, service name, and cross-reference against OS defaults
Architecture Overview
Three-node PostgreSQL cluster: primary + two synchronous replicas. Patroni manages HA and automated failover. HAProxy (or keepalived) provides a virtual IP for reads/writes. PgBouncer sits between applications and HAProxy for connection pooling. pgBackRest handles backup/restore with point-in-time recovery. Prometheus + Grafana collect metrics. All nodes run the same OS and PostgreSQL major version.
Stack
  PostgreSQL 16
  Patroni 3.x + etcd (3-node embedded cluster on same hosts)
  pgBackRest for backup
  PgBouncer for connection pooling
  HAProxy or keepalived for virtual IP
  Prometheus node_exporter + postgres_exporter
  Grafana dashboards
  Systemd for service management
Node Roles
Node A: Primary (initially). Runs Patroni primary, PgBouncer read/write, HAProxy active, pgBackRest primary backup host.
Node B: Replica 1. Runs Patroni replica synchronous, PgBouncher read-only, HAProxy standby.
Node C: Replica 2. Runs Patroni replica synchronous, PgBouncer read-only, HAProxy standby.
Etcd runs on all three nodes as a 3-node embedded cluster stored on a separate disk or partition to avoid I/O contention.
Installation
1. Install PostgreSQL 16 on all three nodes from the official PostgreSQL APT/YUM repository matching the OS distribution.
2. Install Patroni, etcd, PgBouncer, pgBackRest, HAProxy, and Prometheus exporters from distribution packages or pip as appropriate.
3. Initialize the etcd cluster. On each node set ETCD_INITIAL_CLUSTER with all three peers and ETCD_INITIAL_CLUSTER_STATE=new for first bootstrap, existing for subsequent restarts.
4. Configure Patroni on each node with identical namespace, scope, and a unique member name per host. Set synchronous replication with synchronous_mode: true and synchronous_mode_strict: true.
5. Bootstrap the Patroni cluster from Node A. Patroni creates the primary PostgreSQL instance and registers it in etcd. On Node B and C, start Patroni which discovers the cluster and attaches as replicas.
6. Verify replication with psql -c 'select * from pg_stat_replication' on the primary.
PostgreSQL Configuration (included in Patroni config template)
max_connections: 200
shared_buffers: 4GB (25% of RAM on dedicated DB host)
effective_cache_size: 12GB (75% of RAM)
work_mem: 16MB
maintenance_work_mem: 1GB
wal_level: logical (supports both streaming and logical replication)
max_wal_senders: 10
max_replication_slots: 10
wal_keep_size: 4096 (MB)
hot_standby: on
wal_log_hints: on (required for pg_rewind after failover)
track_commit_timestamp: on (required for synchronous replication monitoring)
max_standby_streaming_delay: 30s
wal_buffers: 64MB
random_page_cost: 1.1 (for SSD)
effective_io_concurrency: 200
checkpoint_completion_target: 0.9
Patroni Configuration Template
scope: pg-cluster
namespace: /db/
name: pg-node-a
restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.0.1:8008
  auth: 'patroni:changeme'
etcd:
  host: 127.0.0.1:2379
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
        max_connections: 200
        shared_buffers: 4GB
        wal_level: logical
        wal_log_hints: on
        track_commit_timestamp: on
        hot_standby: on
        max_wal_senders: 10
        max_replication_slots: 10
        wal_keep_size: 4096
        synchronous_commit: remote_write
        synchronous_standby_names: '*'
      recovery_conf:
        restore_command: 'pgbackrest --stanza=db archive-get %f "%p"'
pgbackrest:
  name: db
  create_replica_methods:
    - pgbackrest
  pgbackrest:
    command: pgbackrest --stanza=db restore --delta --db-path=/var/lib/postgresql/16/main
    keep_data: true
    no_params: true
    no_master: 1
postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.0.1:5432
  data_dir: /var/lib/postgresql/16/main
  bin_dir: /usr/lib/postgresql/16/bin
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: changeme
    superuser:
      username: postgres
      password: changeme
    rewind:
      username: rewind_user
      password: changeme
  parameters:
    unix_socket_directories: /var/run/postgresql
    archive_mode: on
    archive_command: 'pgbackrest --stanza=db archive-push %p'
    archive_timeout: 60
Connection Pooling with PgBouncer
Install PgBouncer on each application tier or alongside PostgreSQL on each DB node. The pgbouncer.ini configuration:
[databases]
* = host=127.0.0.1 port=5000
[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 25
max_client_conn = 200
max_db_connections = 50
server_idle_timeout = 600
query_timeout = 30
pkt_buf = 4096
Client applications connect to port 6432 on the local node. PgBouncer forwards to HAProxy port 5000 which handles read/write splitting.
HAProxy Configuration for read-write splitting
/etc/haproxy/haproxy.cfg:
global
  log /dev/log local0
  maxconn 2000
  user haproxy
  group haproxy
  stats socket /var/run/haproxy.sock mode 600 level admin
  stats timeout 30s
defaults
  log global
  mode tcp
  retries 3
  timeout client 30s
  timeout connect 5s
  timeout server 30s
  timeout check 5s
frontend pg_frontend
  bind *:5000
  default_backend pg_backend
backend pg_backend
  option httpchk GET /replica?lag=2048000&lag_window=3&tag=topology
  server pg-node-a 10.0.0.1:5432 check port 8008 inter 10000 rise 2 fall 3
  server pg-node-b 10.0.0.2:5432 check port 8008 inter 10000 rise 2 fall 3
  server pg-node-c 10.0.0.3:5432 check port 8008 inter 10000 rise 2 fall 3
Patroni exposes an HTTP health endpoint on port 8008. HAProxy uses OPTIONS httpchk against that endpoint to determine whether each node is primary, replica, or unhealthy.
Health check interval tuning: inter 10000 checks every 10 seconds. For faster failover detection reduce to inter 3000 (3 seconds) but increase fall to 5 to prevent flapping during brief network pauses. Each check issues OPTIONS /replica?lag=2048000 to Patroni REST API. Patroni returns 200 OK for healthy replicas within lag limit, 503 for lagging or unhealthy nodes. The primary node returns 200 on its own health endpoint.
One httpchk directive per backend is sufficient; do not duplicate it inside server lines.
Virtual IP with keepalived (alternative to HAProxy)
Install keepalived on all three nodes. Configure VIP 10.0.0.100/24 on the Patroni primary via a track script that polls Patroni REST API. Example track script:
vrrp_script check_patroni {
  script "/usr/local/bin/check_patroni.sh"
  interval 2
  fall 2
  rise 2
}
check_patroni.sh:
#!/bin/bash
curl -sf http://127.0.0.1:8008/primary && exit 0 || exit 1
The VIP moves to whichever node Patroni has elected as primary.
Automated Failover
Patroni handles failover internally. When the primary becomes unreachable, etcd detects the lost leader. After ttl=30 seconds, Patroni on a replica holds an election. The replica with the highest LSN and lowest lag wins. Patroni promotes it to primary, then reconfigures synchronous standby names. The former primary, when it recovers, attaches as a replica via pg_rewind.
For manual switchover (planned maintenance):
patronictl -c /etc/patroni/patroni.yml switchover --master pg-node-a --candidate pg-node-b
Monitor the switchover with patronictl -c /etc/patroni/patroni.yml list before and after.
Backup Configuration with pgBackRest
Install pgBackRest on one backup host (Node A or a dedicated backup server). Configure /etc/pgbackrest/pgbackrest.conf:
[db]
pg1-path=/var/lib/postgresql/16/main
pg1-port=5432
[global]
repo1-type=s3
repo1-s3-bucket=my-db-backups
repo1-s3-region=eu-west-1
repo1-s3-endpoint=s3.eu-west-1.amazonaws.com
repo1-path=/pg-cluster/
repo1-retention-full=4
repo1-retention-diff=14
repo1-s3-key-type=auto
compress-type=zst
compress-level=6
process-max=4
archive-async=y
archive-timeout=60
buffer-size=512K
(s3 credentials go in repo1-s3-key and repo1-s3-key-secret via environment variables PGBACKREST_REPO1_S3_KEY and PGBACKREST_REPO1_S3_KEY_SECRET or a separate managed secrets file.)
Create the stanza:
pgbackrest --stanza=db stanza-create
Take a base backup:
pgbackrest --stanza=db --type=full backup
Take a differential backup:
pgbackrest --stanza=db --type=diff backup
Restore to a specific point in time:
pgbackrest --stanza=db restore --delta --pg1-path=/var/lib/postgresql/16/main --type=time --target="2026-06-28 14:30:00+02"
The --delta flag is required when restoring onto a target directory that may contain existing files; it restores only changed files and deletes any extra files not in the backup manifest. The --pg1-path flag specifies the target data directory and must match the actual path on the restore host. On the stanza creation side, pg1-path is the source data directory; on restore, it becomes the destination.
Restore to a new host for cloning or disaster recovery:
pgbackrest --stanza=db restore --delta --pg1-path=/var/lib/postgresql/16/main
After restore, set recovery_target_action=promote in postgresql.auto.conf (automatically done by pgBackRest). Start PostgreSQL to complete recovery. The restored instance is now writable.
Point-in-time recovery flexibility:
  type=time --target='2026-06-27 08:00:00+02' (timestamp recovery)
  type=xid --target=12345678 (transaction ID recovery)
  type=name --target='my_savepoint' (restore point recovery)
  type=lsn --target='0/AB123456' (LSN recovery)
  target-action=promote (automatically end recovery and make instance writable)
Disaster Recovery
Backups & Retention
Retention policy:
  Full backups: one per week, retained for 4 weeks (repo1-retention-full=4)
  Differential backups: one per day, retained for 14 days (repo1-retention-diff=14)
  Archive (WAL) logs: pushed every 60 seconds (archive_timeout=60), retained implicitly by retention-full which keeps all WAL needed for any retained full or diff backup
pgBackRest handles archive expiry automatically during backup operations. The S3 bucket has no additional lifecycle policy — pgBackRest manages retention internally. If required by compliance, add an S3 bucket lifecycle rule with Expiration for objects older than 90 days as a safety net, but note that this may delete backups pgBackRest still references if a full backup retention window exceeds 90 days. Set the S3 lifecycle rule to tag-based expiration, not age-based, and only after aligning retention periods.
Recovery Procedure for Full Site Loss
1. Provision three new nodes with the same OS and PostgreSQL version.
2. Install Patroni, etcd, pgBackRest, and restore dependencies.
3. Configure pgbackrest.conf with the same stanza name and S3 bucket details.
4. Run pgbackrest --stanza=db restore --delta --pg1-path=/var/lib/postgresql/16/main on each node.
5. Start Patroni on all three nodes. The first node to start becomes primary (or manually set with patronictl).
6. Validate replication: check pg_stat_replication on the primary shows two streaming replicas.
For single-node failure within a healthy cluster: Patroni automatically rebuilds the failed replica from the primary using pg_rewind (if the failed node was a primary that was partitioned) or by streaming from the current primary. No manual restore is needed.
Large Database Recovery Considerations
For databases exceeding 500GB, streaming replication rebuild from the primary is faster than pgBackRest restore. To re-sync a replica:
1. On the primary, create a new replication slot: select * from pg_create_physical_replication_slot('replica_b_rebuild')
2. Use pg_basebackup on the replica: pg_basebackup -h primary-host -D /var/lib/postgresql/16/main -S replica_b_rebuild -X stream -P -v
3. Start Patroni on the replica.
For full-site recovery of a 500GB+ database, restore from pgBackRest in parallel using pgbackrest --stanza=db restore --delta --process-max=4 (uses multi-process restore) to reduce recovery time.
Monitoring & Alerting
Patroni Metrics Endpoint
Patroni exposes a comprehensive metrics endpoint at /metrics on port 8008 (or the restapi listen port). Scrape with Prometheus:
scrape_configs:
  - job_name: patroni
    static_configs:
      - targets:
          - 10.0.0.1:8008
          - 10.0.0.2:8008
          - 10.0.0.3:8008
    metrics_path: /metrics
Key Patroni metrics to monitor:
  patroni_primary (1 = primary, 0 = replica) — tracks role transitions
  patroni_replica_lag_bytes — streaming lag in bytes
  patroni_xlog_location — current WAL position for replication health
HAProxy Stats Page
Enable HAProxy stats endpoint in haproxy.cfg for monitoring and load visualization:
frontend stats
  bind *:8404
  stats enable
  stats uri /stats
  stats refresh 10s
  stats auth admin:changeme
  stats admin if TRUE
Prometheus can scrape HAProxy metrics using haproxy_exporter:
  haproxy_exporter --haproxy.scrape-uri='http://admin:changeme@10.0.0.1:8404/stats;csv'
Monitor HAProxy server state transitions to detect failover events.
Streaming Replication Lag Query
The primary source of truth for replication health is pg_stat_replication. Run this query on the primary to detect lag:
select
  application_name,
  state,
  sync_state,
  pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn)) as lag_bytes,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as lag_bytes_raw,
  extract(epoch from now() - replay_lag) as lag_seconds,
  flush_lag,
  replay_lag,
  backend_start
from pg_stat_replication;
Monitor these Prometheus alert rules:
  PG_ReplicaLagBytes > 536870912 (512MB) — ticket severity
  PG_ReplicaLagSeconds > 30 — warnings
  PG_PatroniRoleChange — page on-call (role transitions = failover likely)
  PG_HAPRoxyServerDown > 1 for 5m — alert (one replica unhealthy for too long)
  PG_BackupAge > 30h — warning (full backup overdue if retention policy expects daily full or diff)
Grafana Dashboards
Import or build two dashboards:
1. Database Cluster Overview — shows cluster role, replication lag per node, connections per pooler, backup age, CPU/mem/disk per host
2. Patroni Cluster Detail — shows leader status, timeline, LSN positions, pending restart flags, DCS health
Use postgres_exporter on each node for database-level metrics: connections, queries, cache hit ratio, transaction rate. Prometheus node_exporter provides OS-level metrics.
Systemd Unit Dependencies
Verify service names match the installed distribution. On Debian/Ubuntu the PostgreSQL service is postgresql@16-main, on RHEL it is postgresql-16. The Patroni service is patroni (from package or from script). Check the actual unit name with systemctl list-units --type=service | grep -i postgres before finalizing any systemd dependency directives. Do not assume a service name — look it up on the target OS.
Example working systemd override for Patroni on Ubuntu (confirmed path):
  /etc/systemd/system/patroni.service.d/override.conf
  [Unit]
  Requires=etcd.service
Before writing any systemd dependency, run systemctl cat patroni on the actual node to confirm the unit file uses the expected name and path. On distributions where Patroni is installed via pip without a package manager, the unit file may be missing entirely. Generate it from the Patroni template at /usr/local/lib/python3.x/dist-packages/patroni/patroni.service or write one manually.
Validation Checklist
Before finalizing any deployment or configuration artifact, run these checks:
1. File path check: verify every path in configuration files against the actual OS using ls or test -f. Example: confirm /var/lib/postgresql/16/main exists before setting pg1-path. On RHEL the path is /var/lib/pgsql/16/data.
2. Service name check: run systemctl list-units --type=service | grep -i postgres to find the exact unit name. Do not hardcode postgresql@16-main unless confirmed on the target host.
3. Cross-reference check: ensure every configuration value referenced in one file (e.g. stanza name in archive_command) exactly matches the definition in another file (stanza name in pgbackrest.conf).
4. Distribution match: confirm the PostgreSQL version and package paths match the target distribution. Ubuntu uses /usr/lib/postgresql/16/bin, RHEL uses /usr/pgsql-16/bin.
5. Port consistency: trace every port number across all configuration files — PostgreSQL 5432, Patroni 8008, PgBouncer 6432, HAProxy frontend 5000, etcd 2379 — and ensure no collisions or mismatches.
6. Permission check: verify that the postgres user (or the user running Patroni) can read all config files, write to data_dir, and execute pgbackrest and pg_rewind binaries.
7. auth credentials: confirm that all passwords in Patroni authentication blocks match between pgpass file and the actual PostgreSQL roles. Use psql -c '\du' to list roles and check password hashes.
8. Connectivity test: after initial setup, verify each layer end-to-end: psql to PgBouncer -> PgBouncer to HAProxy -> HAProxy to Patroni-managed PostgreSQL.
9. Failover dry-run: run a manual switchover with patronictl switchover and confirm the virtual IP moves, PgBouncer reconnects, and no queries fail with more than the configured timeout.
10. Restore test: take a full backup, then restore to a separate test host and confirm data integrity with pgbench or a checksum scan.
All items in this validation checklist must be completed and documented before signing off the deployment. Include the validation output (or a link to the CI/CD job log) in the deployment record.