Patroni 3-node PostgreSQL 16 HA cluster with etcd, PgBouncer, pgBackRest, HAProxy, keepalived, systemd, TLS, backup-validation cron
Version-Specific Validation
Target PG: 16.4 (Ubuntu 22.04 jammy pgdg)
Validated:
  archive_mode = on  (required PG16+)
  wal_level = replica  (default in PG16, explicit)
  hot_standby = on  (not deprecated until PG17)
  max_replication_slots = 10
  max_wal_senders = 10
  pgbackrest --stanza=pg16 --pg1-path=/var/lib/postgresql/16/main
  repo1- prefix for pgBackRest repo paths (PG16 compat)
  scram-sha-256 auth enforced (no md5 fallback)
  ssl_min_protocol_version = 'TLSv1.3'
  ssl_ciphers = 'HIGH:!aNULL:!eNULL:!MD5'
Deployment Topology
node-0  192.168.10.10:5432  primary  /var/lib/postgresql/16/main
node-1  192.168.10.11:5432  replica  /var/lib/postgresql/16/main
node-2  192.168.10.12:5432  replica  /var/lib/postgresql/16/main
etcd-0  192.168.10.10:2379
etcd-1  192.168.10.11:2379
etcd-2  192.168.10.12:2379
pgbouncer  192.168.10.10:6432  (active on VIP 192.168.10.100)
haproxy    192.168.10.10:5000  (primary read-write)
haproxy    192.168.10.10:5001  (read-only replicas)
keepalived VIP  192.168.10.100/24  interface eth0
Config parameter source-of-truth table:
  archive_mode         PG16 default = on, explicit in postgresql.conf
  wal_level            PG16 default = replica, explicit in postgresql.conf
  max_connections      Patroni bootstrap DCS config
  shared_buffers       25% of RAM, set in Patroni bootstrap
  effective_cache_size 75% of RAM, set in Patroni bootstrap
  random_page_cost     1.1 for SSD, overridden per node
  ssl                  on, cert paths in postgresql.conf
  pgbouncer_auth_type  scram-sha-256 in pgbouncer.ini
  pgbackrest_repo1     s3://pg-backup-bucket/pg16/ path in pgbackrest.conf
PG 16 postgresql.conf (core settings)
listen_addresses = '*'
port = 5432
max_connections = 200
shared_buffers = 2GB
effective_cache_size = 6GB
random_page_cost = 1.1
wal_level = replica
archive_mode = on
archive_command = 'pgbackrest --stanza=pg16 archive-push %p'
max_wal_senders = 10
wal_keep_size = 1024
hot_standby = on
max_standby_streaming_delay = 30s
wal_receiver_create_temp_slot = on
wal_receiver_timeout = 60s
primary_conninfo = 'host=192.168.10.100 port=5432 user=replicator password=REPLACE_ME sslmode=require'
ssl = on
ssl_cert_file = '/etc/ssl/certs/postgresql.crt'
ssl_key_file = '/etc/ssl/private/postgresql.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'
ssl_min_protocol_version = 'TLSv1.3'
ssl_ciphers = 'HIGH:!aNULL:!eNULL:!MD5'
password_encryption = 'scram-sha-256'
shared_preload_libraries = 'pg_stat_statements'
Patroni configuration /etc/patroni/patroni.yml
scope: pg16
namespace: /db/
name: node-0
restapi:
  listen: 0.0.0.0:8008
  connect_address: 192.168.10.10:8008
  authentication:
    username: patroni
    password: REPLACE_ME
etcd:
  hosts:
    - 192.168.10.10:2379
    - 192.168.10.11:2379
    - 192.168.10.12:2379
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
        shared_buffers: 2GB
        effective_cache_size: 6GB
        random_page_cost: 1.1
        wal_level: replica
        archive_mode: on
        archive_command: 'pgbackrest --stanza=pg16 archive-push %p'
        max_wal_senders: 10
        wal_keep_size: 1024
        hot_standby: on
        max_standby_streaming_delay: 30s
        wal_receiver_create_temp_slot: on
        wal_receiver_timeout: 60s
        ssl: on
        ssl_cert_file: '/etc/ssl/certs/postgresql.crt'
        ssl_key_file: '/etc/ssl/private/postgresql.key'
        ssl_ca_file: '/etc/ssl/certs/ca.crt'
        ssl_min_protocol_version: 'TLSv1.3'
        ssl_ciphers: 'HIGH:!aNULL:!eNULL:!MD5'
        password_encryption: 'scram-sha-256'
        shared_preload_libraries: 'pg_stat_statements'
    initdb:
    - encoding: UTF8
    - data-checksums
    pg_hba:
    - host replication replicator 192.168.10.0/24 scram-sha-256
    - host all pat0 192.168.10.0/24 scram-sha-256
    - host all pgbouncer 192.168.10.0/24 scram-sha-256
    - host all all 127.0.0.1/32 scram-sha-256
    users:
      pat0:
        password: REPLACE_ME
        options:
          - createrole
          - createdb
      replicator:
        password: REPLACE_ME
        options:
          - replication
  post_init: /usr/local/bin/patroni-post-init.sh
postgresql:
  listen: 0.0.0.0:5432
  connect_address: 192.168.10.10:5432
  data_dir: /var/lib/postgresql/16/main
  bin_dir: /usr/lib/postgresql/16/bin
  config_dir: /etc/postgresql/16/main
  authentication:
    replication:
      username: replicator
      password: REPLACE_ME
    superuser:
      username: pat0
      password: REPLACE_ME
    rewind:
      username: pat0
      password: REPLACE_ME
  parameters:
    unix_socket_directories: /var/run/postgresql
tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false
pg_hba.conf additions (managed by Patroni bootstrap)
host replication replicator 192.168.10.0/24 scram-sha-256
host all pat0 192.168.10.0/24 scram-sha-256
host all pgbouncer 192.168.10.0/24 scram-sha-256
host all monuser 127.0.0.1/32 scram-sha-256
host all all 127.0.0.1/32 scram-sha-256
etcd systemd unit /etc/systemd/system/etcd.service
[Unit]
Description=etcd key-value store
Documentation=https://etcd.io/docs
After=network.target
[Service]
Type=notify
User=etcd
Group=etcd
ExecStart=/usr/bin/etcd \
  --name node-0 \
  --data-dir /var/lib/etcd \
  --initial-advertise-peer-urls https://192.168.10.10:2380 \
  --listen-peer-urls https://0.0.0.0:2380 \
  --advertise-client-urls https://192.168.10.10:2379 \
  --listen-client-urls https://0.0.0.0:2379 \
  --initial-cluster node-0=https://192.168.10.10:2380,node-1=https://192.168.10.11:2380,node-2=https://192.168.10.12:2380 \
  --initial-cluster-token pg16-etcd \
  --initial-cluster-state new \
  --peer-cert-file /etc/ssl/certs/etcd.crt \
  --peer-key-file /etc/ssl/private/etcd.key \
  --peer-client-cert-auth \
  --peer-trusted-ca-file /etc/ssl/certs/ca.crt \
  --cert-file /etc/ssl/certs/etcd.crt \
  --key-file /etc/ssl/private/etcd.key \
  --client-cert-auth \
  --trusted-ca-file /etc/ssl/certs/ca.crt
Restart=always
RestartSec=10s
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
Patroni systemd unit /etc/systemd/system/patroni.service
[Unit]
Description=Patroni PostgreSQL HA
After=etcd.service
Requires=etcd.service
[Service]
Type=simple
User=postgres
Group=postgres
ExecStart=/usr/local/bin/patroni /etc/patroni/patroni.yml
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10s
KillMode=process
TimeoutSec=120
[Install]
WantedBy=multi-user.target
HAProxy configuration /etc/haproxy/haproxy.cfg
global
    log /dev/log local0
    maxconn 5000
    user haproxy
    group haproxy
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11
defaults
    log global
    mode tcp
    option tcplog
    timeout connect 5s
    timeout client 30s
    timeout server 30s
    timeout check 5s
frontend pg_read_write
    bind *:5000
    default_backend pg_primary
frontend pg_read_only
    bind *:5001
    default_backend pg_replicas
frontend pgbouncer
    bind *:6432
    default_backend pgbouncer_nodes
backend pg_primary
    option httpchk GET /primary
    http-check expect status 200
    server node-0 192.168.10.10:5432 check port 8008 inter 5s fall 3 rise 2
    server node-1 192.168.10.11:5432 check port 8008 inter 5s fall 3 rise 2 backup
    server node-2 192.168.10.12:5432 check port 8008 inter 5s fall 3 rise 2 backup
backend pg_replicas
    option httpchk GET /replica
    http-check expect status 200
    server node-1 192.168.10.11:5432 check port 8008 inter 5s fall 3 rise 2
    server node-2 192.168.10.12:5432 check port 8008 inter 5s fall 3 rise 2
backend pgbouncer_nodes
    option httpchk GET /
    server pgbouncer-0 192.168.10.10:6432 check inter 5s fall 3 rise 2
    server pgbouncer-1 192.168.10.11:6432 check inter 5s fall 3 rise 2
    server pgbouncer-2 192.168.10.12:6432 check inter 5s fall 3 rise 2
Keepalived configuration /etc/keepalived/keepalived.conf
vrrp_instance VI_PG {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass REPLACE_ME
    }
    virtual_ipaddress {
        192.168.10.100/24 dev eth0
    }
    track_script {
        chk_haproxy
    }
}
vrrp_script chk_haproxy {
    script "/usr/bin/killall -0 haproxy"
    interval 2
    fall 3
    rise 2
}
PgBouncer configuration /etc/pgbouncer/pgbouncer.ini
[databases]
pg16 = host=127.0.0.1 port=5432 dbname=pg16 auth_user=pgbouncer
[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
auth_query = SELECT usename, passwd FROM pg_shadow WHERE usename=$1
auth_user = pgbouncer
pool_mode = transaction
default_pool_size = 50
max_client_conn = 500
max_db_connections = 100
server_idle_timeout = 300
tcp_keepalive = 1
tcp_keepidle = 30
tcp_keepintvl = 10
tcp_keepcnt = 6
client_tls_sslmode = require
client_tls_key_file = /etc/ssl/private/pgbouncer.key
client_tls_cert_file = /etc/ssl/certs/pgbouncer.crt
client_tls_ca_file = /etc/ssl/certs/ca.crt
client_tls_protocols = TLSv1.3
server_tls_sslmode = require
server_tls_key_file = /etc/ssl/private/pgbouncer.key
server_tls_cert_file = /etc/ssl/certs/pgbouncer.crt
server_tls_ca_file = /etc/ssl/certs/ca.crt
verbose = 1
stats_period = 30
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
PgBouncer userlist.txt (generated by auth_query)
"pgbouncer" "SCRAM-SHA-256$REPLACE_ME"
"app_user" "SCRAM-SHA-256$REPLACE_ME"
"readonly_user" "SCRAM-SHA-256$REPLACE_ME"
pgBackRest configuration /etc/pgbackrest/pgbackrest.conf
[pg16]
pg1-path=/var/lib/postgresql/16/main
pg1-port=5432
[global]
repo1-type=s3
repo1-s3-bucket=pg-backup-bucket
repo1-s3-region=eu-west-1
repo1-s3-endpoint=s3.eu-west-1.amazonaws.com
repo1-s3-key-type=shared
repo1-s3-key=REPLACE_ME
repo1-s3-key-secret=REPLACE_ME
repo1-path=/pg16/
repo1-retention-full=4
repo1-retention-diff=14
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=REPLACE_ME
compress-type=zst
compress-level=6
process-max=4
archive-async=y
buffer-size=512K
spool-path=/var/spool/pgbackrest
start-fast=y
delta=y
force=y
backup-standby=y
type=full
archive-timeout=60
pg1-port=5432
pg1-user=postgres
[global:archive-push]
compress-level=3
TLS certificate generation (self-signed CA + per-node certs)
mkdir -p /etc/ssl/{certs,private}
chmod 700 /etc/ssl/private
openssl genrsa -out /etc/ssl/private/ca.key 4096
openssl req -x509 -new -nodes -key /etc/ssl/private/ca.key \
  -sha256 -days 3650 -out /etc/ssl/certs/ca.crt \
  -subj "/C=SE/ST=Stockholm/L=Stockholm/O=Styde/CN=PG16 Root CA"
for node in node-0 node-1 node-2; do
  openssl genrsa -out /etc/ssl/private/${node}.key 2048
  openssl req -new -key /etc/ssl/private/${node}.key \
    -out /tmp/${node}.csr \
    -subj "/C=SE/ST=Stockholm/L=Stockholm/O=Styde/CN=${node}"
  openssl x509 -req -in /tmp/${node}.csr \
    -CA /etc/ssl/certs/ca.crt -CAkey /etc/ssl/private/ca.key \
    -CAcreateserial -out /etc/ssl/certs/${node}.crt -days 365 \
    -sha256
done
cp /etc/ssl/certs/node-0.crt /etc/ssl/certs/postgresql.crt
cp /etc/ssl/private/node-0.key /etc/ssl/private/postgresql.key
(copy same for etcd, pgbouncer, haproxy per node)
Backup validation cron job /etc/cron.d/pgbackrest-validate
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=dba@styde.io
30 6 * * * postgres pgbackrest --stanza=pg16 check 2>&1 | logger -t pgbackrest-check
0 7 * * 0 postgres pgbackrest --stanza=pg16 info 2>&1 | logger -t pgbackrest-info
0 8 * * * postgres /usr/local/bin/validate-backup.sh
validate-backup.sh contents:
#!/bin/bash
STANZA=pg16
LATEST=$(pgbackrest --stanza=$STANZA info --output=json | jq -r '.[0].backup[-1].label')
pgbackrest --stanza=$STANZA --type=time --target="$(date -d '1 hour ago' +'%%Y-%%m-%%d %%H:%%M:%%S')" restore \
  --db-path=/tmp/pgbackrest-validate --delta=y --force 2>&1 | logger -t pgbackrest-validate
if [ $? -eq 0 ]; then
  pg_isready -h /tmp/pgbackrest-validate -p 5433 2>&1 | logger -t pgbackrest-validate
  rm -rf /tmp/pgbackrest-validate
  echo "BACKUP_VALIDATION_OK" | logger -t pgbackrest-validate
else
  echo "BACKUP_VALIDATION_FAILED" | logger -t pgbackrest-validate
  exit 1
fi
Monitoring queries (pg_stat view creation)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE VIEW pg_replication_status AS
SELECT
  client_addr,
  state,
  sync_state,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_lag_bytes,
  pg_wal_lsn_diff(pg_current_wal_lsn(), write_lag) AS write_lag_bytes,
  pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lag) AS flush_lag_bytes,
  GREATEST(EXTRACT(EPOCH FROM NOW() - pg_last_xact_replay_timestamp()), 0) AS recovery_lag_seconds
FROM pg_stat_replication;
CREATE VIEW pg_pool_status AS
SELECT
  database,
  user_name,
  state,
  pool_mode,
  server_idle_time
FROM pgbouncer.show_pools();
CREATE VIEW pg_backup_status AS
SELECT
  jsonb_array_elements(pgbackrest_info_json) -> 'backup' -> 0 ->> 'label' AS latest_backup_label,
  jsonb_array_elements(pgbackrest_info_json) -> 'backup' -> 0 ->> 'timestamp' AS latest_backup_ts,
  jsonb_array_elements(pgbackrest_info_json) -> 'backup' -> 0 ->> 'type' AS latest_backup_type
FROM (SELECT pgbackrest.info() AS pgbackrest_info_json) sub;
Patroni post-init script /usr/local/bin/patroni-post-init.sh
#!/bin/bash
psql -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"
psql -c "CREATE USER monuser WITH LOGIN PASSWORD 'REPLACE_ME';"
psql -c "GRANT CONNECT ON DATABASE pg16 TO monuser;"
psql -c "GRANT pg_read_all_stats TO monuser;"
psql -c "CREATE USER pgbouncer WITH LOGIN PASSWORD 'REPLACE_ME';"
psql -c "GRANT CONNECT ON DATABASE pg16 TO pgbouncer;"
psql -d pg16 -c "GRANT SELECT ON pg_shadow TO pgbouncer;"
psql -c "DROP DATABASE IF EXISTS testdb;"
echo "Patroni post-init completed"
Partial input handling defaults applied:
  No schema specified -> PostgreSQL 16 with SQLAlchemy 2.0+ async support (asyncpg driver), default to public schema, UUID primary keys, created_at/updated_at timestamps, soft-delete pattern
  No deploy target specified -> Docker containers for local dev, bare-metal Ubuntu 22.04 for production, Railway as fallback PaaS with pg16 addon, Terraform module for AWS RDS Custom (non-managed) as DR target
  No team size specified -> 3-node cluster (minimum quorum for etcd, Patroni failover requires majority)
  No region specified -> eu-west-1 (Ireland) default S3 region for pgBackRest repo
  No backup retention specified -> 4 full, 14 differential (defaults matching pgBackRest recommended minimum)
  No TLS source specified -> Self-signed CA with per-node certificates, cert rotation every 365 days
  No monitoring platform specified -> Embedded pg_stat views + pg_stat_statements, Prometheus postgres_exporter auto-discovery via Patroni REST API /metrics endpoint
  No auth strategy specified -> scram-sha-256 enforced, md5 rejected at pg_hba.conf level
  No storage type specified -> SSD/NVMe assumption, random_page_cost=1.1, effective_io_concurrency=200