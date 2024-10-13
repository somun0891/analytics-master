WITH prep_ci_build AS (

    SELECT 

    --Surrogate key
      dim_ci_build_sk,

      --Legacy Natural Key
      dim_ci_build_id, 

      --NATURAL KEY
      ci_build_id,
      
      -- FOREIGN KEYS
      dim_project_id,
      dim_namespace_id,
      ultimate_parent_namespace_id,
      created_date_id,
      dim_plan_id,
      dim_ci_runner_id,
      dim_user_id,
      dim_ci_stage_id,

      ci_build_status,
      finished_at,
      created_at,
      updated_at,
      started_at,
      coverage,
      commit_id,
      ci_build_name,
      options,
      allow_failure,
      stage,
      trigger_request_id,
      stage_idx,
      tag,
      ref,
      ci_build_type,
      ci_build_description,
      erased_by_id,
      erased_at,
      artifacts_expire_at,
      environment,
      queued_at,
      lock_version,
      coverage_regex,
      auto_canceled_by_id,
      retried,
      protected,
      failure_reason,
      failure_reason_id,
      scheduled_at,
      upstream_pipeline_id
    FROM {{ ref('prep_ci_build') }}

)

{{ dbt_audit(
    cte_ref="prep_ci_build",
    created_by="@mpeychet_",
    updated_by="@lisvinueza",
    created_date="2021-06-17",
    updated_date="2024-08-28"
) }}

