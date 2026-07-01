feedback:
  session: previous
  runs:
    - score: 85.6
      status: production_gate_cleared
      issues:
        - dimension: completeness
          judge_score: 78
          blockers:
            - pre_submit_placeholders_check_missing
            - markdown_only_output_no_file_writing
            - azure_vmss_field_mapping_wrong
            - config_yaml_duplicate_entries
      required_fixes:
        - file: BLUEPRINT.md
          action: add_pre_submit_placeholder_check
          pattern: \$\{[A-Z]+\}
          reject_on_match: true
        - file: BLUEPRINT.md
          action: replace_output_format
          old: present as embedded markdown blocks
          new: write output to target file paths
        - file: BLUEPRINT.md
          action: fix_azure_vmss_field_mapping
          field: ultraSSDEnabled
          error: currently maps to Spot
          correct_path: verify_azure_vmss_query_spec
        - file: config.yaml
          action: deduplicate_versionhistory
          dedup_key: versionhistory
    - score: 80.8
      session: 20260628-150239
      status: below_production_threshold
      weakest_dimension: accuracy
      severity: high
      blockers:
        - deprecated_cli_syntax_az_vmss
        - deprecated_cli_syntax_aws_spot
        - unresolved_placeholders_in_output
      required_fixes:
        - file: BLUEPRINT.md
          action: add_placeholder_check_section
          scope: pre_submit
          pattern: \$\{.*?\}
          behavior: reject_output_containing_unresolved_variables
        - file: skills/azure-cost-management
          action: fix_az_vmss_command
          old: az vmss show --query 'virtualMachineProfile.storageProfile...provisioningState'
          new: az vmss list-instances --query
          also_fix: az monitor condition simplified_syntax_to_current_spec
        - file: skills/aws-cost-management
          action: rewrite_spot_request_examples
          old_syntax: --spot-price/--launch-specification
          new_syntax: --instance-market-options
        - file: BLUEPRINT.md
          action: add_execution_verification_step
          method: run_each_cli_command_against_dry_run_or_help_before_output
  composite_diagnosis:
    root_causes:
      - pre_submit_validation_missing
      - stale_cli_syntax_two_clouds
      - markdown_only_output_instead_of_file_io
      - template_placeholders_left_unresolved
    priority_order:
      1: placeholder_check
      2: execution_verification
      3: fix_azure_vmss_command
      4: fix_aws_spot_syntax
      5: output_format_file_writing
      6: deduplicate_config_yaml