{{ config(
    tags=["product"]
) }}

WITH prep_ci_runner AS (

  SELECT

    -- SURROGATE KEY
    dim_ci_runner_sk,

    --NATURAL KEY
    ci_runner_id,

    --LEGACY NATURAL KEY
    dim_ci_runner_id,

    -- FOREIGN KEYS
    created_date_id,
    created_at,
    updated_at,
    ci_runner_description,

    --- CI Runner Manager Mapping
    CASE
      --- Private Runners
      WHEN ci_runner_description ILIKE '%private%manager%'
        THEN 'private-runner-mgr'
      --- Linux Runners
      WHEN ci_runner_description ILIKE 'shared-runners-manager%'
        THEN 'linux-runner-mgr'
      WHEN ci_runner_description ILIKE '%.shared.runners-manager.%'
        THEN 'linux-runner-mgr'
      WHEN ci_runner_description ILIKE '%saas-linux-%-amd64%'
        AND ci_runner_description NOT ILIKE '%shell%'
        THEN 'linux-runner-mgr'
      --- Internal GitLab Runners
      WHEN ci_runner_description ILIKE 'gitlab-shared-runners-manager%'
        THEN 'gitlab-internal-runner-mgr'
      --- Window Runners 
      WHEN ci_runner_description ILIKE 'windows-shared-runners-manager%'
        THEN 'windows-runner-mgr'
      --- Shared Runners
      WHEN ci_runner_description ILIKE '%.shared-gitlab-org.runners-manager.%'
        THEN 'shared-gitlab-org-runner-mgr'
      --- macOS Runners
      WHEN LOWER(ci_runner_description) ILIKE '%macos%'
        THEN 'macos-runner-mgr'
      --- Other
      ELSE 'Other'
    END         AS ci_runner_manager,

    --- CI Runner Machine Type Mapping
    ci_runner_machine_type,
    cost_factor,
    contacted_at,
    is_active,
    ci_runner_version,
    revision,
    platform,
    is_untagged,
    is_locked,
    access_level,
    maximum_timeout,
    ci_runner_type,
    CASE ci_runner_type
      WHEN 1 THEN 'shared'
      WHEN 2 THEN 'group-runner-hosted runners'
      WHEN 3 THEN 'project-runner-hosted runners'
    END         AS ci_runner_type_summary,
    public_projects_minutes_cost_factor,
    private_projects_minutes_cost_factor

  FROM {{ ref('prep_ci_runner') }}

)

{{ dbt_audit(
    cte_ref="prep_ci_runner",
    created_by="@snalamaru",
    updated_by="@lisvinueza",
    created_date="2021-06-23",
    updated_date="2024-08-28"
) }}
