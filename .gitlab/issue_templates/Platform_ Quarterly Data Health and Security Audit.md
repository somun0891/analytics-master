# Quarterly Data Health and Security Audit

Quarterly audit is performed to validate security like right people with right access in environments (Example: Sisense, Snowflake.etc) and data feeds that are running are healthy (Example: Salesforce, GitLab.com..etc).

Please see the [handbook page](https://about.gitlab.com/handbook/business-technology/data-team/data-management/#quarterly-data-health-and-security-audit) for more information. 

Below checklist of activities would be run once for quarter to validate security and system health. Recommend to convert all steps to seperate tasks. 

## SNOWFLAKE
1. [ ] Snowflake: Validate terminated employees have been removed from Snowflake access. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/snowflake.md#validate-terminated-employees-have-been-removed-from-snowflake-access)
2. [ ] Snowflake: De-activate any account that has not logged-in within the past 60 days from the moment of performing audit from Snowflake. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/snowflake.md#de-activate-any-account-that-has-not-logged-in-within-the-past-60-days-from-the-moment-of-performing-audit-from-snowflake)
3. [ ] Snowflake: Validate all user accounts do not have password set. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/snowflake.md#validate-all-user-accounts-do-not-have-password-set)
4. [ ] Snowflake: Drop orphaned tables. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/snowflake.md#drop-orphaned-tables)

## DBT Execution
1. [ ] DBT Execution: Generate report on top 25 long running dbt models. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/dbt.md)
 
## AIRFLOW
1. [ ] Airflow: Validate off-boarded employees have been removed from Airflow access. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/airflow.md#validate-off-boarded-employees-have-been-removed-from-airflow-access)
1. [ ] Airflow: Clean up log files [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/airflow.md#clean-up-old-log-files)

## Monte Carlo
1. [ ] Monte Carlo: Validate off-boarded employees have been removed from Monte Carlo access. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/montecarlo.md#validate-off-boarded-employees-have-been-removed-from-monte-carlo-access)
1. [ ] Monte Carlo: Deprovision access if an account has not logged-in within the past 90 days from the moment of performing audit. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/montecarlo.md#deprovision-access-if-an-account-has-not-logged-in-within-the-past-90-days-from-the-moment-of-performing-audit)

## Tableau
1. [ ] Tableau: Validate offboarded employess have been removed from Tableau Cloud and purge from systems: [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/tableau.md#validate-offboarded-employees-have-been-removed-from-tableau-cloud-and-purge-from-systems)

1. [ ] Tableau: Deprovision access if a user has had access for >=90 days, but have not logged in during the past 90 days from the moment of performing audit: [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/tableau.md#deprovision-access-if-a-user-has-had-access-for-90-days-but-have-not-logged-in-during-the-past-90-days-from-the-moment-of-performing-audit)

1. [ ] Tableau: Downgrade Inactive Role Users: [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/tableau.md#downgrade_inactive_role_users)

1. [ ] Tableau: Role Credentials for Snowflake Service Accounts: [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/tableau/update_service_account_password.md?ref_type=heads)

## Package version inventory

1. [ ] Python and other tools/libraries inventory. [Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/quarterly_data_health_and_security_audit/package_inventory.md#package-version-inventory)


<!-- DO NOT EDIT BELOW THIS LINE -->
/label ~"Team::Data Platform" ~Snowflake ~TDF ~"Data Team" ~"Priority::1-Ops" ~"workflow::4 - scheduled" ~"Quarterly Data Health and Security Audit" ~"Periscope / Sisense"
/confidential 
