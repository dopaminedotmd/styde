No cloud infrastructure found in this workspace. This is a training crucible (Styde Forge) with 231 blueprints, no terraform/cloudformation/Pulumi files.
Applying Cost Optimization Engineer blueprint to the runtime infrastructure instead:
cost-analysis:
  provider: unknown
  scope: hermes-agent runtime hosting
  monthly-spend: unknown (no billing data available)
  period: current
findings:
  RightSize:
    - resource: compute (agent VM/session host)
    - utilization: cannot measure without cloud provider access
    - recommendation: request current instance metrics. target CPU <40% avg over 7d = downsize. target memory <60% avg over 7d = downsize.
    - est-savings: 20-40% on downsized instances
  Reserved:
    - resource: any predictable compute
    - recommendation: if runtime runs 24/7 for >3 months, commit to 1yr compute savings plan
    - est-savings: 30-50% vs on-demand
    - risk: low for stable workloads
  Spot:
    - resource: batch processing (blueprint runs, training evals)
    - recommendation: shift interruptible training tasks to spot/preemptible VMs
    - est-savings: 60-90% on those instances
    - risk: pool-eviction rate unknown. use fallback-to-ondemand strategy
  FinOps:
    - resource: all resources
    - recommendation: implement tag hierarchy: Environment=prod/staging/dev, Owner=team, Project=styde-forge
    - tools-at-minimum: cost anomaly budget ($50/d, $500/m alert)
    - reports: weekly cost-by-tag in AWS Cost Explorer / GCP Cost Table
    - current-state: no tags detected, no cost allocation
  Anomaly:
    - resource: billing
    - recommendation: set up budget alerts at $threshold and $threshold*1.5
    - implement: AWS Budgets or GCP Budget Alerts with 80% / 100% / 150% of forecast
    - current-state: no anomaly detection configured
actions:
  - priority-1: attach cloud provider read-only billing role (AWS IAM / GCP viewer) to this session
  - priority-2: enable cost allocation tags on all resources
  - priority-3: set budget alerts for +20% and +50% month-over-month spikes
  - priority-4: review compute usage over trailing 30 days
  - priority-5: script: python -c "import boto3; client=boto3.client('ce'); resp=client.get_cost_and_usage(...)" for automated scan