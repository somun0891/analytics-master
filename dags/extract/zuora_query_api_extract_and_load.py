import os
import yaml
from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow_utils import (
    DATA_IMAGE,
    clone_and_setup_extraction_cmd,
    gitlab_defaults,
    slack_failed_task,
    gitlab_pod_env_vars,
    REPO_BASE_PATH,
)
from kube_secrets import (
    GCP_SERVICE_CREDS,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_LOAD_PASSWORD,
    SNOWFLAKE_LOAD_ROLE,
    SNOWFLAKE_LOAD_USER,
    SNOWFLAKE_LOAD_WAREHOUSE,
    ZUORA_API_CLIENT_ID,
    ZUORA_API_CLIENT_SECRET,
)
from kubernetes_helpers import get_affinity, get_toleration

# Load the env vars into a dict and set Secrets
env = os.environ.copy()
pod_env_vars = gitlab_pod_env_vars

# Default arguments for the DAG
default_args = {
    "depends_on_past": False,
    "on_failure_callback": slack_failed_task,
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "sla": timedelta(hours=24),
    "sla_miss_callback": slack_failed_task,
    "start_date": datetime(2021, 6, 1),
    "dagrun_timeout": timedelta(hours=6),
}


# Create the DAG
dag = DAG(
    "zuora_query_api_extract_and_load",
    default_args=default_args,
    schedule_interval="0 3 * * *",
    concurrency=2,
    catchup=False,
)


def extract_manifest(file_path):
    with open(file_path, "r") as file:
        manifest_dict = yaml.load(file, Loader=yaml.FullLoader)
    return manifest_dict


manifest = extract_manifest(f"{REPO_BASE_PATH}/extract/zuora_query_api/src/queries.yml")
tables = manifest.get("tables")

for table_name in tables:
    extract_command = f"""
        {clone_and_setup_extraction_cmd} &&
            python zuora_query_api/src/main.py tap zuora_query_api/src/queries.yml --load_only_table {table_name}
    """
    task_identifier = f"{table_name.replace('_', '-')}"

    zuora_data_query_extract = KubernetesPodOperator(
        **gitlab_defaults,
        image=DATA_IMAGE,
        task_id=task_identifier,
        name=task_identifier,
        secrets=[
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_LOAD_ROLE,
            SNOWFLAKE_LOAD_USER,
            SNOWFLAKE_LOAD_WAREHOUSE,
            SNOWFLAKE_LOAD_PASSWORD,
            ZUORA_API_CLIENT_ID,
            ZUORA_API_CLIENT_SECRET,
        ],
        env_vars=pod_env_vars,
        affinity=get_affinity("extraction"),
        tolerations=get_toleration("extraction"),
        arguments=[extract_command],
        dag=dag,
    )
