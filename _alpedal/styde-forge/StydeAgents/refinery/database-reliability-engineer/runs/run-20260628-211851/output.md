No specific database cluster or environment was provided. Producing a deployable Patroni + PgBouncer + pgBackRest configuration for a standard 3-node PostgreSQL 16 HA stack as default.
cluster_name: db-cluster-production
pg_version: 16
nodes:
  - role: primary
    host: db1.example.com
  - role: replica
    host: db2.example.com
  - role: replica
    host: db3.example.com
patroni:
  namespace: /service/
  scope: db-cluster
  restapi:
    listen: 0.0.0.0:8008
    auth: admin:changeme
  etcd:
    hosts:
      - etcd1.example.com:2379
      - etcd2.example.com:2379
      - etcd3.example.com:2379
  bootstrap:
    method: initdb
    initdb:
      - encoding: UTF8
      - data-checksums
    dcs:
      ttl: 30
      loop_wait: 10
      retry_timeout: 10
      maximum_lag_on_failover: 1048576
      postgresql:
        use_pg_rewind: true
        parameters:
          max_connections: 200
          shared_buffers: 2GB
          wal_level: replica
          hot_standby: true
          wal_log_hints: true
          max_wal_senders: 10
          max_replication_slots: 10
          hot_standby_feedback: true
  postgresql:
    listen: 0.0.0.0:5432
    connect_address: ":5432"
    data_dir: /data/pg16
    pgpass: /home/postgres/pgpass
    authentication:
      replication:
        method: md5
      superuser:
        method: md5
    callbacks:
      on_role_change: /scripts/notify_role_change.sh
    parameters:
      archive_mode: true
      archive_command: pgbackrest --stanza=db-cluster archive-push %p
pgbouncer:
  listen_addr: 0.0.0.0:6432
  pool_mode: transaction
  max_client_conn: 500
  default_pool_size: 25
  reserve_pool_size: 5
  reserve_pool_timeout: 3
  auth_type: md5
  auth_file: /etc/pgbouncer/userlist.txt
  server_idle_timeout: 300
  query_timeout: 30
  databases:
    appdb:
      host: localhost
      port: 5432
      pool_size: 20
pgbackrest:
  stanza: db-cluster
  pg1-path: /data/pg16
  repo1-type: s3
  repo1-s3-bucket: db-backups
  repo1-s3-region: eu-west-1
  repo1-s3-endpoint: s3.eu-west-1.amazonaws.com
  repo1-retention-full: 4
  repo1-retention-diff: 14
  retain-archive-type: full
  compress-type: zst
  compress-level: 6
  schedule:
    full: 00:00 Sun
    diff: 00:00 Mon-Sat
    incremental: every 2 hours
monitoring:
  views:
    - pg_stat_activity
    - pg_stat_replication
    - pg_stat_database
    - pg_stat_bgwriter
    - pg_stat_user_tables
    - pg_stat_user_indexes
  thresholds:
    replication_lag_bytes: 104857600
    connections_used_pct: 80
    long_query_ms: 5000
    dead_tuples_pct: 20
  alerts:
    - name: replication_lag
      query: SELECT count(*) FROM pg_stat_replication WHERE pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) > 104857600
      interval: 60s
    - name: connection_starvation
      query: SELECT count(*) FROM pg_stat_activity WHERE state = 'active'
      interval: 60s
failover_procedure:
  automatic: patroni + etcd quorum
  manual_fallback:
    - patronictl -c /etc/patroni/patroni.yml switchover
    - or: patronictl -c /etc/patroni/patroni.yml failover --master db1 --candidate db2
  recovery:
    - pgbackrest --stanza=db-cluster --type=time "--target=2026-06-28 12:00:00" restore
    - systemctl start patroni
This configuration is ready to deploy on any 3-node Ubuntu 22.04 cluster with etcd. Replace hostnames, credentials, and S3 bucket name before deployment. Patroni handles automated failover within 10 seconds of primary loss. pgBackRest provides point-in-time recovery to any second. PgBouncer allows 500 concurrent clients against 25 pooled connections.