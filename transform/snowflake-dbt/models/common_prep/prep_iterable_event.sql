{{ simple_cte([
    ('iterable_event_source', 'iterable_event_source') 
]) }}

, final AS (

    SELECT
        {{ dbt_utils.generate_surrogate_key(['iterable_event_fivetran_id','iterable_user_fivetran_id']) }} AS iterable_event_unique_id,
        iterable_event_fivetran_id, 
        iterable_user_fivetran_id,
        iterable_event_campaign_id,
        iterable_event_message_id,
        iterable_event_content_id,
        iterable_event_created_at,
        iterable_event_name,
        iterable_event_ip,
        is_iterable_custom_event,
        iterable_event_message_bus_id,
        iterable_event_message_type_id,
        iterable_event_recipient_state,
        iterable_event_status,
        iterable_event_unsubscribe_source,
        iterable_event_user_agent,
        iterable_event_user_agent_device,
        iterable_event_transactional_data,
        iterable_event_additional_properties
    FROM iterable_event_source

)

SELECT *
FROM final