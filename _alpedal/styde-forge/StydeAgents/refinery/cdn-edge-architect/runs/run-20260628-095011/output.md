accuracy self-flag is critical for CDN infrastructure where wrong numbers cost real money
verify-hard-numbers step mandatory before emitting any concrete dollar amount, ASN, IP range, or provider name
cross-check against source or annotate with ~approximate and confidence qualifier
YAML lint pass mandatory before final output: run yaml.safeload on output string, reject on YAMLError, regenerate
no hand-written YAML keys: use exact key:value format from schema
preload yaml validator helper in skill: call safeload before writing final output
verify-hard-numbers section:
  domain: devops
  blueprint: cdn-edge-architect
  steps:
    - for each concrete dollar amount: cross-check against published pricing page or invoice
    - for each ASN: verify via bgp.he.net or ripe stat
    - for each IP range: verify via whois/rdap
    - for each company name: verify via official site or crunshbase
    - annotate: confidence < 100% -> tag with ~approximate and brief confidence qualifier
    - output: yaml block, run through yaml.safeload before delivery