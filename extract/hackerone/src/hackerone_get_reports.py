"""
Extract HackerOne reports from the HackerOne API.
"""

import json
import os
import sys
from datetime import datetime
from logging import basicConfig, error, getLogger, info
from time import sleep
from typing import Dict, Tuple, Union

import requests
from gitlabdata.orchestration_utils import (
    snowflake_engine_factory,
    snowflake_stage_load_copy_remove,
)

config_dict = os.environ.copy()
HEADERS = {
    "Accept": "application/json",
}
TIMEOUT = 60
BASE_URL = "https://api.hackerone.com/v1/"
HACKERONE_API_USERNAME = config_dict.get("HACKERONE_API_USERNAME")
HACKERONE_API_TOKEN = config_dict.get("HACKERONE_API_TOKEN")
RECORD_THRESHOLD = 2000


def get_start_and_end_date() -> Tuple[str, str]:
    """
    This function will get the start and end date
    """
    # set start date as yesterdays date time and end data as todays date(start of the day at 00:00:00hrs) , if a full refresh is required then a default date will be set
    is_full_refresh = os.environ["is_full_refresh"]
    info(f"Full refresh is set to : {is_full_refresh}")

    if is_full_refresh.lower() == "true":
        start_date = "2020-01-01T00:00:00Z"
    else:
        data_interval_start = os.environ["data_interval_start"]
        start_date = datetime.strptime(
            data_interval_start, "%Y-%m-%dT%H:%M:%S%z"
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
    data_interval_end = os.environ["data_interval_end"]
    end_date = datetime.strptime(data_interval_end, "%Y-%m-%dT%H:%M:%S%z").strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    return start_date, end_date


def upload_events_to_snowflake(events) -> None:
    """Upload event payload to Snowflake"""
    upload_dict = {"data": events}

    schema_name = "hackerone"
    stage_name = "hackerone_load_stage"
    table_name = "reports"
    json_dump_filename = "hackerone_reports.json"
    upload_payload_to_snowflake(
        upload_dict, schema_name, stage_name, table_name, json_dump_filename
    )


def upload_payload_to_snowflake(
    payload: Dict,
    schema_name: str,
    stage_name: str,
    table_name: str,
    json_dump_filename: str = "to_upload.json",
):
    """
    Upload payload to Snowflake using snowflake_stage_load_copy_remove()
    """
    info("Uploading payload to Snowflake")
    loader_engine = snowflake_engine_factory(config_dict, "LOADER")
    with open(json_dump_filename, "w+", encoding="utf8") as upload_file:
        json.dump(payload, upload_file)

    snowflake_stage_load_copy_remove(
        json_dump_filename,
        f"{schema_name}.{stage_name}",
        f"{schema_name}.{table_name}",
        loader_engine,
    )
    loader_engine.dispose()


def nullify_vulnerability_information(report_data):
    """
    This function will nullify the vulnerability information
    """
    info("Nullifying vulnerability_information")
    if "bounties" in report_data:
        for bounty in report_data["bounties"]:
            if "relationships" in bounty:
                if (
                    "report" in bounty["relationships"]
                    and "data" in bounty["relationships"]["report"]
                ):
                    if "attributes" in bounty["relationships"]["report"]["data"]:
                        bounty["relationships"]["report"]["data"]["attributes"][
                            "vulnerability_information"
                        ] = "None"

    return report_data


def get_reports(start_date: str, end_date: str):
    """
    This function will get the reports from hackerone
    """
    info(f"Getting reports from {start_date} to {end_date}")
    reports_list = []
    page = 1
    while True:
        info(f"Getting reports, extracting page {page}")
        params: Dict[str, Union[int, str]] = {
            "filter[program][]": "gitlab",
            "page[number]": page,
            "page[size]": 100,
            "filter[last_activity_at__gt]": start_date,
            "filter[last_activity_at__lt]": end_date,
        }
        response = requests.get(
            f"{BASE_URL}reports",
            headers=HEADERS,
            params=params,
            auth=(HACKERONE_API_USERNAME, HACKERONE_API_TOKEN),
            timeout=TIMEOUT,
        )
        if response.status_code == 200:
            response_json = response.json()
            for report in response_json["data"]:
                report_data = {
                    "id": report["id"],
                    "state": report["attributes"]["state"],
                    "created_at": report["attributes"]["created_at"],
                    "bounties": report["relationships"]["bounties"]["data"],
                }
            report_data = nullify_vulnerability_information(report_data)
            reports_list.append(report_data)
            info(f"current length of reports {len(reports_list)}")
            if (
                len(reports_list) >= RECORD_THRESHOLD
            ):  # if record threshold is reached, upload to snowflake
                info(
                    f"Reached record threshold of {RECORD_THRESHOLD}, uploading records to snowflake"
                )
                upload_events_to_snowflake(reports_list)
                reports_list = []

            if "next" not in response_json["links"]:
                break
            page += 1  # move on to the next set of paginated results(cursor based paginated)
        elif (
            response.status_code == 429
        ):  # if we hit rate limit, wait 60 seconds and try again
            info(
                f"Rate limit exceeded: {response.status_code}, waiting for 60 seconds before sending another request"
            )
            sleep(60)
        else:
            error(f"Error getting reports: {response.status_code}")
            sys.exit(1)

    return reports_list


def main() -> None:
    """Main function."""
    # set start date and end date
    start_date, end_date = get_start_and_end_date()
    # get reports from endpoint
    reports_list = get_reports(start_date, end_date)
    # upload payload to snowflake
    upload_events_to_snowflake(reports_list)


if __name__ == "__main__":
    basicConfig(stream=sys.stdout, level=20)
    getLogger("snowflake.connector.cursor").disabled = True
    main()
    info("Complete.")
