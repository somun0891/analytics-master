"""
Extract and load Elasticsearch billing itemized costs
"""

import os
from datetime import date, datetime, timedelta
from logging import info

from utility import (
    get_response,
    prep_dataframe,
    upload_to_snowflake,
    get_extraction_start_date_end_date_backfill,
    get_extraction_start_date_end_date_recon,
    get_response_and_upload,
)

config_dict = os.environ.copy()
org_id = config_dict["ELASTIC_CLOUD_ORG_ID"]
table_name = "itemized_costs"


def get_itemized_costs():
    """
    Get Itemized costs from Elastic Cloud API from start of current month till present date
    """

    info("Getting itemized costs from Elastic Cloud API")
    date_today = datetime.utcnow().date()
    if date_today.day == 1:
        extraction_start_date = date_today - timedelta(days=1)
        extraction_start_date = extraction_start_date.replace(day=1)
    else:
        extraction_start_date = date_today.replace(day=1)
    extraction_end_date = date_today - timedelta(days=1)
    itemised_costs_url = f"/billing/costs/{org_id}/items?from={extraction_start_date}&to={extraction_end_date}"
    get_response_and_upload(
        itemised_costs_url, extraction_start_date, extraction_end_date, table_name
    )


def get_reconciliation_data():
    """
    Get reconciliation data from Elastic Cloud API,
    It is performed on 7 and 14th of every month for the previous month to capture any billing corrections
    """

    date_today = datetime.utcnow().date()
    # if date_today day is 7 or 14 then set extraction_start_date as previous months start date and extraction_end_date as previous months end date
    if date_today.day in [3, 7, 14, 15]:
        info("Performing reconciliation...")
        (
            extraction_start_date,
            extraction_end_date,
        ) = get_extraction_start_date_end_date_recon(date_today)
        itemised_costs_url = f"/billing/costs/{org_id}/items?from={extraction_start_date}&to={extraction_end_date}"
        get_response_and_upload(
            itemised_costs_url, extraction_start_date, extraction_end_date, table_name
        )

    else:
        info("No reconciliation required")


def get_itemized_costs_backfill():
    """
    Get Itemized costs from Elastic Cloud API from start date provided by dag config till previous months_end_date
    """
    (
        extraction_start_date,
        extraction_end_date,
    ) = get_extraction_start_date_end_date_backfill()
    info(
        f"Extraction starting from date {extraction_start_date} till date {extraction_end_date}"
    )
    output_list = []
    # iterate each month in between extraction_start_date and extraction_end_date and call API
    for year in range(extraction_start_date.year, extraction_end_date.year + 1):
        for month in range(1, 13):
            current_month = date(year, month, 1)
            start_date = current_month
            if month != 12:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            else:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            if start_date >= extraction_start_date and end_date <= extraction_end_date:
                info(f"{start_date} till {end_date}")
                itemised_costs_url = (
                    f"/billing/costs/{org_id}/items?from={start_date}&to={end_date}"
                )
                data = get_response(itemised_costs_url)
                row_list = [
                    data,
                    start_date,
                    end_date,
                ]
                output_list.append(row_list)
    # upload this data to snowflake
    columns_list = [
        "payload",
        "extraction_start_date",
        "extraction_end_date",
    ]
    output_df = prep_dataframe(output_list, columns_list)
    upload_to_snowflake(output_df, table_name)


def extract_load_billing_itemized_costs():
    """
    Extract and load Elastic Search Billing itemized costs from start of current month till present date and perform reconciliation
    """

    # Regular daily load from start of current month date till present date
    info("Beginning extraction of Elastic Search Billing itemized costs")
    get_itemized_costs()
    # Capture reconciliation data for previous month
    get_reconciliation_data()
    info("Extraction completed for Elastic Search Billing itemized costs")
