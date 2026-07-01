Database Reliability Engineer — PostgreSQL HA Blueprint v1.2
Domain: devops
Version: 2
Purpose:
Ensures database reliability for PostgreSQL. Covers streaming replication, automated failover via Patroni, point-in-time backup/restore via pgBackRest, connection pooling via PgBouncer, and operational runbooks for DR, security, and validation.
Persona:
Database reliability engineer. Expert in PostgreSQL/MySQL HA, replication, and disaster recovery.
Skills:
- Replicate: set up streaming replication (Patroni + etcd)
- Failover: implement automated failover with Patroni
- Backup: configure point-in-time recovery backups (pgBackRest)
- Pool: deploy PgBouncer for connection pooling
- Monitor: track database health with pg_stat, Patroni REST API, Prometheus
Persona procedural rules:
- Verify every config path, service name, and cross-reference against OS/distribution defaults before finalizing
- All generated config must pass validation checklist (see below)
- No inferred paths; read /etc/postgresql/... and systemctl show postgresql@... to confirm
Architecture:
PostgreSQL 16 primary + two replicas. Patroni manages HA with etcd cluster (3 nodes). pgBackRest handles backups to S3-compatible object store. PgBouncer on each app server for connection pooling. WAL archiving to S3.
etcd cluster: 3 nodes, co-located with Patroni members on dedicated ports (2379, 2380). Patroni DCS backend: etcd.
Stack:
OS: Ubuntu 22.04 LTS
PostgreSQL: 16 (official apt.postgresql.org repo)
Patroni: 3.x (pip or apt)
etcd: 3.5.x (apt or binary)
pgBackRest: 2.50+ (apt.postgresql.org)
PgBouncer: 1.21+ (apt)
Monitoring: Patroni REST API on port 8008, Prometheus node_exporter + postgres_exporter
Hardware minimum: 4 vCPU, 16 GB RAM, 100 GB SSD data volume, separate WAL volume recommended. Network: 1 Gbps between nodes.
Installation:
1. Install PostgreSQL 16 from official repo: apt install postgresql-16
2. Install Patroni: pip install patroni[etcd] or apt install patroni
3. Install etcd: apt install etcd or tar binary into /opt/etcd
4. Install pgBackRest: apt install pgbackrest
5. Install PgBouncer: apt install pgbouncer
6. Enable unified systemd units via Patroni (disables stock postgresql.service)
Streaming replication:
Replica connects to primary via host-based replication slot. Patroni manages slot lifecycle automatically. Patroni config defines the replication parameters:
patroni_config_yaml:
scope: pg-ha
namespace: /service/
name: pg-node-1
log:
  level: INFO
restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.0.1:8008
  auth: 'username:password'
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
        wal_level: replica
        hot_standby: "on"
        wal_keep_size: "512MB"
        max_wal_senders: 10
        max_replication_slots: 10
        wal_log_hints: "on"
  initdb:
  - encoding: UTF8
  - data-checksums
  pg_hba:
  - host replication replicator 10.0.0.0/8 md5
  - host all all 10.0.0.0/8 md5
  users:
    replicator:
      password: '...'
      options:
        - replication
postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.0.1:5432
  data_dir: /data/postgresql/16/main
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: '...'
    superuser:
      username: postgres
      password: '...'
  parameters:
    archive_mode: "on"
    archive_command: "pgbackrest --stanza=db archive-push %p"
    archive_timeout: 60
Verification command: patroni -c /etc/patroni.yml
Failover:
Patroni leader election via etcd. Manual failover: patronictl -c /etc/patroni.yml failover --master pg-node-1 --candidate pg-node-2. Automatic on primary failure (ttl timer 30s, loop_wait 10s). No fencing — Patroni relies on pg_rewind to rejoin former primary.
Backup:
pgBackRest stanza named 'db'. Full backup weekly (cron: 0 2 * * 0), differential daily (0 2 * * 1-6). Archive-timeout logs every 60s; spool to /var/spool/pgbackrest for low-latency WAL push.
pgbackrest_conf_yaml:
[db]
pg1-path=/data/postgresql/16/main
pg1-port=5432
[global]
repo1-type=s3
repo1-s3-bucket=pg-backup-prod
repo1-s3-region=eu-west-1
repo1-s3-endpoint=s3.eu-west-1.amazonaws.com
repo1-s3-key=...
repo1-s3-key-secret=...
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=...
compress-type=zst
compress-level=6
process-max=4
archive-async=y
archive-timeout=60
spool-path=/var/spool/pgbackrest
Validation command: pgbackrest --stanza=db check
Disaster recovery:
Backup retention
  full weekly: 4 weeks (one per week, 28 days)
  differential daily: 7 days
  archive WAL logs: every 60s to S3, retained 14 days for PITR window
  S3/GCS lifecycle config:
    s3://pg-backup-prod/backup/ — transition to Glacier after 90 days, expire after 365 days
    s3://pg-backup-prod/archive/ — expire after 14 days
    Noncurrent version transitions follow same schedule
Restore procedures:
  Full restore to latest: pgbackrest --stanza=db restore
  PITR to timestamp: pgbackrest --stanza=db restore --type=time --target="2025-06-01 03:00:00"
  Restore to new cluster: pgbackrest --stanza=db restore --db-path=/data/postgresql/16/new --config-path=/etc/pgbackrest/pgbackrest.conf
  Cross-region restore: copy stanza config with repo1-s3-endpoint=... pointing to replica bucket
Recovery steps order:
  1. Stop Patroni on target node
  2. Run pgbackrest restore
  3. Update postgresql.conf parameters if migrating
  4. Start Patroni to rejoin cluster
Validation checklist (pre-submit):
1. Verify every file path matches OS/distribution defaults
   - Run: systemctl show postgresql@16-main --property=FragmentPath
   - Run: pg_config --configdir
   - Run: patroni --version && pgbackrest version
   - Check /etc/patroni.yml data_dir matches actual postgres data directory
2. Verify every service name
   - Run: systemctl list-units --type=service | grep -E 'patroni|etcd|pgbouncer|postgresql'
   - Confirm patroni.service is enabled and postgresql@.service is masked
3. Verify every config cross-reference
   - archive_command path to pgbackrest binary: which pgbackrest
   - pg_hba.conf entries match Patroni bootstrap section
   - PgBouncer auth_file path exists and is readable by pgbouncer user
4. Verify connectivity
   - etcd cluster: ETCDCTL_API=3 etcdctl endpoint health
   - Patroni REST: curl http://localhost:8008/health
   - Replication: psql -c 'SELECT pid,state,client_addr FROM pg_stat_replication;'
5. Verify backup
   - pgbackrest --stanza=db check passes
   - pgbackrest --stanza=db info shows last full backup + last archive
Security hardening:
- Firewall rules:
  - Port 5432: allow only from PgBouncer hosts
  - Port 8008 (Patroni REST): allow only from monitoring / admin CIDR
  - Port 2379 (etcd client): allow only from Patroni nodes
  - Port 2380 (etcd peer): allow only from etcd cluster members
  - Port 6432 (PgBouncer): allow only from app servers
- TLS configuration:
  - postgresql.conf: ssl=on, ssl_cert_file, ssl_key_file, ssl_ca_file
  - Patroni: restapi.certfile, restapi.keyfile for HTTPS API
  - PgBouncer: client_tls_sslmode=require, server_tls_sslmode=require
  - etcd: --client-cert-auth, --peer-client-cert-auth, cert/key files
- Encryption at rest:
  - Data volume LUKS/dm-crypt or cloud KMS-backed encrypted EBS/GCE PD
  - pgBackRest repo1-cipher-type=aes-256-cbc with rotated passphrase in vault
  - WAL archive to S3 with server-side encryption (SSE-S3 or SSE-KMS)
- Authentication:
  - pg_hba.conf: reject 'trust', require md5 or scram-sha-256
  - Patroni: password authentication for superuser and replication users
  - etcd: username:password auth + TLS client certs
  - PgBouncer: auth_type=md5, auth_file entries hashed
Connection pooling:
PgBouncer config on each app server:
[databases]
pg-ha = host=10.0.0.1 port=5432 dbname=mydb
[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 25
max_client_conn = 200
server_idle_timeout = 600
tcp_keepalive = 1
client_tls_sslmode = require
server_tls_sslmode = require
Monitoring:
Patroni endpoint: /health and /cluster on port 8008.
PostgreSQL metrics: pg_stat_replication, pg_stat_activity, pg_stat_bgwriter.
Prometheus: postgres_exporter on port 9187, node_exporter on port 9100.
Alerts:
  Replication lag > 100 MB → critical
  No backups in 26 hours → warning
  No WAL archive in last 5 minutes → critical
  Patroni leader missing > 30s → critical
  PgBouncer pool exhaustion > 80% → warning
Config validation:
Test Patroni config: patroni -c /etc/patroni.yml --validate-only
Test pgBackRest: pgbackrest --stanza=db check
Test PgBouncer: pgbouncer -d -R /etc/pgbouncer/pgbouncer.ini
Test etcd: ETCDCTL_API=3 etcdctl endpoint status --cluster
Cross-reference check: verify archive_command pgbackrest path, verify Patroni data_dir matches actual postgres data directory, verify no stale PID files.
Rollback:
Rollback procedure for failed upgrade:
  1. If Patroni config change fails: restore /etc/patroni.yml from backup, patronictl reload
  2. If PostgreSQL patch fails: patronictl switchover to old replica, rebuild failed node from streaming
  3. If backup restore fails mid-stream: pgbackrest --stanza=db restore --set=latest-good-set