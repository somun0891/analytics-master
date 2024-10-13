{% docs rpt_delta_arr_parent_month_8th_calendar_day %}

This report provides the 8th calendar day snapshot for the mart_delta_arr_parent_month table. It uses the rpt_delta_arr_parent_month_8th_calendar_day to build the table.

Custom Business Logic:

1. The parent/child crm account hierarchy changes on a monthly basis. The ARR snapshot table captures the account hierarchy on the 8th calendar day. When doing month over month calcs, this can result in accounts showing as churn in the snapshot data, but in reality, they just changed account hierarchies and did not churn. Therefore, we use the live crm account hierarchy in this model to remove the error that results from looking at snapshot account hierarchies.

2. We started snapshotting the product ranking in August 2022. Therefore, we have to use the live product ranking to backfill the data. In the future, this can be refined to use a dim_product_detail snapshot table when it is built.

{% enddocs %}

{% docs rpt_delta_arr_parent_product_month_8th_calendar_day %}

This report provides the 8th calendar day snapshot for the mart_delta_arr_parent_product_month table. It uses the rpt_delta_arr_parent_month_8th_calendar_day to build the table.

Custom Business Logic:

1. The parent/child crm account hierarchy changes on a monthly basis. The ARR snapshot table captures the account hierarchy on the 8th calendar day. When doing month over month calcs, this can result in accounts showing as churn in the snapshot data, but in reality, they just changed account hierarchies and did not churn. Therefore, we use the live crm account hierarchy in this model to remove the error that results from looking at snapshot account hierarchies.

2. We started snapshotting the product ranking in August 2022. Therefore, we have to use the live product ranking to backfill the data. In the future, this can be refined to use a dim_product_detail snapshot table when it is built.

{% enddocs %}


{% docs rpt_crm_opportunity_renewal %}

This report model focuses exclusively on filtering out Renewal Opportunities from `mart_crm_opportunity`.

{% enddocs %}


{% docs rpt_crm_opportunity_open %}

This report model focuses exclusively on filtering out all Open Opportunities from `mart_crm_opportunity`.

{% enddocs %}

{% docs rpt_stage_progression %}

This report provides a detailed timeline for each opportunity, including when it entered each stage, the duration it stayed in each stage, and its final outcome (Won, Lost, or Open).

Each row represents a unique opportunity, recording the dates it entered each stage and the duration spent in each stage.

- STAGE_CATEGORY indicates the final status ("Won", "Open" or "Lost").
- CREATED_DATE is when the opportunity was created.
- CREATE_DAYS shows the time from creation to the first stage.
- For each stage (STAGE0 to STAGE7), the report includes the entry date and days spent in that stage.
- CLOSE_DATE marks when the opportunity was closed.
- CURRENT_DAYS tracks how long an open opportunity has remained in its current stage.

{% enddocs %}
