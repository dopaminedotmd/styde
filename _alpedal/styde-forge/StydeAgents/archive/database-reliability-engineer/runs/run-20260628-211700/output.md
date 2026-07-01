Database reliability engineer active. PostgreSQL/MySQL HA, replication, disaster recovery.
Current task: no specific database system identified. No connection strings provided. No cluster state given.
Prerequisites missing:
- Database type (PostgreSQL / MySQL / both)
- Server addresses
- Authentication credentials
- Current replication status
- OS package manager
Required inputs to proceed with any action:
Replicate:
- Primary host:port
- Standby host:port
- PostgreSQL version
- WAL archiving method
Failover:
- Patroni config template needed
- DCS (etcd/consul/zookeeper) endpoints
- Number of replicas
Backup:
- pg_dump or pg_basebackup target path
- Retention policy
- S3 or local storage
Pool:
- PgBouncer config: pool_mode, max_client_conn, default_pool_size
- Application connection strings
Monitor:
- pg_stat_activity queries
- Nagios / Prometheus endpoint
- Alert thresholds
Provide inputs. I will execute the full stack.