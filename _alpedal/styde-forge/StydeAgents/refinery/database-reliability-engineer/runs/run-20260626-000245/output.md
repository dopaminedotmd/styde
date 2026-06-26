Database Reliability Engineer persona loaded. Skills active: Replicate, Failover, Backup, Pool, Monitor.
No target database specified. State what needs doing:
Streaming replication setup — provide primary IP, replication slot name, standby count.
Patroni failover — provide cluster config path and DCS endpoint (etcd/consul).
PITR backup — provide WAL archive destination and retention policy.
PgBouncer pool — provide max client connections and pool mode (session/transaction/statement).
Monitor — provide target host. I will query pg_stat_replication, pg_stat_activity, and replication lag in real time.
One command and it runs.