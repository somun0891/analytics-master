{{ simple_cte([
    ('iterable_campaign_history_source', 'iterable_campaign_history_source'),
    ('iterable_campaign_list_history_source', 'iterable_campaign_list_history_source'),
    ('iterable_campaign_suppression_list_history_source', 'iterable_campaign_suppression_list_history_source')
]) }}

, final AS ( 

    SELECT
        {{ dbt_utils.generate_surrogate_key(['iterable_campaign_history_source.iterable_campaign_id','iterable_campaign_history_source.iterable_campaign_updated_at']) }} AS iterable_campaign_unique_id,
        iterable_campaign_history_source.iterable_campaign_id,
        iterable_campaign_history_source.iterable_campaign_updated_at,
        iterable_campaign_history_source.iterable_campaign_updated_date,
        iterable_campaign_history_source.iterable_campaign_template_id,
        iterable_campaign_history_source.iterable_recurring_campaign_id,
        iterable_campaign_history_source.iterable_campaign_state,
        iterable_campaign_history_source.iterable_campaign_created_at,
        iterable_campaign_history_source.iterable_campaign_created_date,
        iterable_campaign_history_source.iterable_campaign_created_by_user_id,
        iterable_campaign_history_source.iterable_campaign_ended_at,
        iterable_campaign_history_source.iterable_campaign_ended_date,
        iterable_campaign_history_source.iterable_campaign_name,
        iterable_campaign_history_source.iterable_campaign_type,
        iterable_campaign_history_source.iterable_campaign_message_medium,
        iterable_campaign_history_source.iterable_campaign_workflow_id,
        ARRAY_AGG(iterable_campaign_list_history_source.iterable_campaign_list_id) AS iterable_campaign_list_id_array,
        ARRAY_AGG(iterable_campaign_suppression_list_history_source.iterable_campaign_suppressed_list_id) AS iterable_campaign_suppression_list_id_array
    FROM iterable_campaign_history_source
    LEFT JOIN iterable_campaign_list_history_source
        ON iterable_campaign_history_source.iterable_campaign_id=iterable_campaign_list_history_source.iterable_campaign_id
            AND iterable_campaign_history_source.iterable_campaign_updated_date=iterable_campaign_list_history_source.iterable_campaign_list_updated_date
    LEFT JOIN iterable_campaign_suppression_list_history_source
        ON iterable_campaign_history_source.iterable_campaign_id=iterable_campaign_suppression_list_history_source.iterable_campaign_id
            AND iterable_campaign_history_source.iterable_campaign_updated_date=iterable_campaign_suppression_list_history_source.iterable_campaign_list_updated_date
    {{dbt_utils.group_by(n=16)}}

)

SELECT *
FROM final