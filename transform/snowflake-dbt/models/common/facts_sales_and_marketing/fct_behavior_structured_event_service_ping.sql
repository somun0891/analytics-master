{{
  config(
    materialized='incremental',
    unique_key='behavior_structured_event_pk',
    on_schema_change = "sync_all_columns",
    tags=["product", "mnpi_exception"]
  )
}}

WITH redis_clicks AS (
  SELECT
    behavior_structured_event_pk,
    behavior_at, 
    gsc_pseudonymized_user_id,
    dim_namespace_id,
    dim_project_id,
    gsc_plan,
    redis_event_name,
    key_path,
    data_source
  FROM {{ ref('fct_behavior_structured_event') }}
  WHERE has_gitlab_service_ping_context = TRUE
  AND is_staging_event = FALSE
  AND behavior_at >= '2022-11-01' -- no events added to SP context before Nov 2022

  {% if is_incremental() %}
  
    AND behavior_at >= (SELECT MAX(behavior_at) FROM {{this}})
  
  {% endif %}
),

namespaces_hist AS (
  SELECT
    *
  FROM {{ ref('gitlab_dotcom_namespace_lineage_scd') }}
),

final AS (
  SELECT
    redis_clicks.behavior_structured_event_pk,
    redis_clicks.behavior_at,
    redis_clicks.gsc_pseudonymized_user_id,
    redis_clicks.dim_namespace_id,
    redis_clicks.dim_project_id,
    redis_clicks.gsc_plan,
    namespaces_hist.ultimate_parent_id AS ultimate_parent_namespace_id,
    redis_clicks.redis_event_name,
    redis_clicks.key_path,
    redis_clicks.data_source
  FROM redis_clicks
  LEFT JOIN namespaces_hist ON namespaces_hist.namespace_id = redis_clicks.dim_namespace_id
    AND redis_clicks.behavior_at BETWEEN namespaces_hist.lineage_valid_from AND namespaces_hist.lineage_valid_to
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@mdrussell",
    updated_by="@utkarsh060",
    created_date="2022-12-21",
    updated_date="2024-03-22"
) }}