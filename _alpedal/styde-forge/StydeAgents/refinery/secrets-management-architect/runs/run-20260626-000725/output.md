Ready. Secrets Management Architect online.
Vault, SOPS, external-secrets, rotation, audit. State your infrastructure. Bare metal, K8s, hybrid. I adapt the stack.
Single command to deploy Vault dev on K8s:
helm repo add hashicorp https://helm.releases.hashicorp.com && helm install vault hashicorp/vault --set server.dev.enabled=true
Production path: HA with Raft storage, auto-unseal via cloud KMS, audit to stdout + file sink.
SOPS for GitOps: encrypt with age key. age-keygen -o ~/.config/sops/age/key.txt. sops --encrypt secrets.yaml.
External-secrets operator: ClusterSecretStore points to Vault. ExternalSecret pulls to K8s Secret. Sync interval, rewrite strategy, deletion policy.
Rotation: Vault database secrets engine. Static roles + TTL. Cron job calls vault write <path>/rotate-role/<name>.
Audit: vault audit enable file file_path=/vault/audit/audit.log. Ship with fluentbit. Alert on repeated 403s.
State your infra. I narrow to your stack.