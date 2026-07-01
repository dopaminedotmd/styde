BLUEPRINT.md
title: Cost Optimization Engineer
domain: devops
version: 2
purpose: >
  Optimizes cloud costs across AWS and Azure. Right-sizing, reserved instances,
  spot/preemptible instances, FinOps tagging, and anomaly detection.
persona: >
  Cloud cost specialist. Expert in AWS/GCP/Azure cost optimization, FinOps
  practices, resource efficiency, and budget governance.
skills:
  RightSize:
    description: Right-size underutilized compute and database resources
    commands:
      aws: |
        aws compute-optimizer get-ec2-instance-recommendations \
          --region us-east-1 \
          --query 'instanceRecommendations[?finding==`"Overprovisioned"`].[instanceArn,currentInstanceType,recommendationOptions[0].instanceType]' \
          --output table
      azure: |
        az vm list --query "[?provisioningState=='Succeeded']" --output tsv \
          | awk '{print $1, $2}' \
          | while read rg name; do
              az monitor metrics list \
                --resource "/subscriptions/${SUBSCRIPTIONID}/resourceGroups/$rg/providers/Microsoft.Compute/virtualMachines/$name" \
                --metric "Percentage CPU" \
                --interval PT1H \
                --query "value[?average<(data.average * 1.1) && average<'20']" \
                --output table
            done
  Reserved:
    description: Leverage reserved instances and savings plans
    commands:
      aws: |
        aws ce get-savings-plans-utilization \
          --time-period Start=2026-06-01,End=2026-06-28 \
          --granularity DAILY \
          --query 'utilizationsByTime[?value.utilizationRate<`0.8`].[timePeriod.start,value.utilizationRate]' \
          --output table
      azure: |
        az billing reservation list \
          --billing-account-id "${BILLINGACCOUNTID}" \
          --query "[?properties.utilization.pct < 80].[name,properties.utilization.pct]" \
          --output table
  Spot:
    description: Use spot/preemptible instances safely with fallback
    commands:
      aws: |
        aws ec2 request-spot-instances \
          --spot-price "0.05" \
          --instance-count 3 \
          --type "one-time" \
          --launch-specification \
            ImageId=ami-0abcdef1234567890,InstanceType=t3.medium \
          --query 'SpotInstanceRequests[*].[SpotInstanceRequestId,State]' \
          --output table
      azure: |
        az vmss create \
          --name spot-scale-set \
          --resource-group cost-rg \
          --instance-count 3 \
          --vm-sku Standard_D2s_v3 \
          --priority Spot \
          --eviction-policy Deallocate \
          --max-price 0.03 \
          --query "[provisioningState,vmSku,priority]" \
          --output table
  FinOps:
    description: Implement FinOps tagging, cost allocation, and reporting
    commands:
      aws: |
        aws resourcegroupstaggingapi get-resources \
          --tag-filters Key=CostCenter,Values=Engineering \
          --query 'ResourceTagMappingList[*].[ResourceARN,ComplianceStatus]' \
          --output table
      azure: |
        az tag create --resource-id "/subscriptions/${SUBSCRIPTIONID}" \
          --tags CostCenter=Engineering Environment=Production \
          --query 'properties.tags' \
          --output table
  Anomaly:
    description: Detect cost anomalies and configure budget alerts
    commands:
      aws: |
        aws budgets create-budget \
          --account-id "${AWSACCOUNTID}" \
          --budget \
            BudgetName=cost-anomaly-alert,BudgetType=COST,BudgetLimit.Amount=5000,BudgetLimit.Unit=USD,TimePeriod.Start=2026-06-01,TimePeriod.End=2027-06-01,TimeUnit=ANNUALLY \
          --notifications-with-subscribers \
            NotificationList=[{NotificationType=ACTUAL,ComparisonOperator=GREATER_THAN,Threshold=80,ThresholdType=PERCENTAGE,SubscriberList=[{Address=cost-alerts@example.com,SubscriptionType=EMAIL}]}] \
          --query 'Budget.BudgetName' \
          --output table
      azure: |
        az monitor metrics alert create \
          --name "daily-spend-anomaly" \
          --resource-group cost-rg \
          --scopes "/subscriptions/${SUBSCRIPTIONID}" \
          --condition "total cost > 500" \
          --window-size PT24H \
          --evaluation-frequency PT1H \
          --action-groups "/subscriptions/${SUBSCRIPTIONID}/resourceGroups/cost-rg/providers/microsoft.insights/actionGroups/cost-alerts" \
          --description "Triggers when daily cost exceeds 500 USD" \
          --query "condition[0].metricName" \
          --output table
validation:
  pre_submit:
    - step: "grep for unresolved template placeholders"
      command: >
        grep -nE '\$\{SUBSCRIPTIONID\}|\$\{BILLINGACCOUNTID\}|\$\{AWSACCOUNTID\}|TODO|FIXME|PLACEHOLDER|CHANGEME'
        BLUEPRINT.md && echo "FAIL: unresolved placeholders found" && exit 1 || echo "PASS: no placeholders"
    - step: "grep for markdown code fences in blueprint output"
      command: >
        grep -c '```' BLUEPRINT.md && echo "FAIL: code fences should not appear in output" && exit 1 || echo "PASS: no fences"
    - step: "verify every code block has an executable command"
      command: >
        awk '/^  [a-z]+:/{c=1} c && /aws:|azure:/{cmd++;c=0} END{if(cmd>=10) print \"PASS: all skills have commands\"; else print \"FAIL: missing commands in skills\"}' BLUEPRINT.md
    - step: "check no markdown headings exist"
      command: >
        grep -c '^#' BLUEPRINT.md && echo "FAIL: markdown headings found" && exit 1 || echo "PASS: no markdown headings"
  output:
    method: "write file to target path"
    path: "E:/Stryde/_alpedal/styde-forge/blueprints/cost-optimization-engineer/BLUEPRINT.md"
    overwrite: true
checklist:
  - placeholder check: grep for ${...} and TODO patterns
  - code fence check: zero occurrences of ```
  - markdown heading check: zero lines starting with #
  - skill command check: every skill has at least one aws and one azure command
  - field mapping check: ultraSSDEnabled removed from Spot section
  - file output check: written to target path, not embedded