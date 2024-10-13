{{ simple_cte([
    ('iterable_message_type_source', 'iterable_message_type_source'),
    ('iterable_user_unsubscribed_message_type_source', 'iterable_user_unsubscribed_message_type_source')
]) }}

, final AS (

    SELECT
        iterable_message_type_source.iterable_message_type_id,
        iterable_user_unsubscribed_message_type_source.iterable_user_fivetran_id,
        iterable_message_type_source.iterable_message_name,
        iterable_message_type_source.iterable_message_channel_id,
        iterable_message_type_source.iterable_message_created_at,
        iterable_message_type_source.iterable_message_created_date,
        iterable_message_type_source.iterable_message_rate_limit_per_minute,
        iterable_message_type_source.iterable_message_subscription_policy,
        MAX(iterable_message_type_source.iterable_message_updated_at)  AS iterable_message_updated_at_last
    FROM iterable_message_type_source
    LEFT JOIN iterable_user_unsubscribed_message_type_source
        ON iterable_message_type_source.iterable_message_type_id=iterable_user_unsubscribed_message_type_source.iterable_unsubscribed_message_type_id
    {{dbt_utils.group_by(n=8)}}

)

SELECT *
FROM final