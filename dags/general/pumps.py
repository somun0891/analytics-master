import os
from datetime import datetime, timedelta
from yaml import safe_load, YAMLError

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow_utils import (
    DATA_IMAGE,
    clone_repo_cmd,
    gitlab_defaults,
    slack_failed_task,
    REPO_BASE_PATH,
)
from kube_secrets import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_LOAD_DATABASE,
    SNOWFLAKE_LOAD_WAREHOUSE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_USER,
)
from kubernetes_helpers import get_affinity, get_toleration

# Load the env vars into a dict and set Secrets
env = os.environ.copy()
GIT_BRANCH = env["GIT_BRANCH"]
pod_env_vars = {
    "CI_PROJECT_DIR": "/analytics",
    "SNOWFLAKE_PROD_DATABASE": "PROD",
}

# Default arguments for the DAG
default_args = {
    "depends_on_past": False,
    "on_failure_callback": slack_failed_task,
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": datetime(2021, 3, 14),
    "dagrun_timeout": timedelta(hours=1),
}

# Create the DAG
dag = DAG(
    "data_pumps",
    default_args=default_args,
    schedule_interval="0 5 * * *",
    catchup=False,
)

with open(f"{REPO_BASE_PATH}/pump/pumps.yml", "r") as file:
    try:
        stream = safe_load(file)
    except YAMLError as exc:
        print(exc)

    pumps = stream["pumps"]


logical_date = "{{ logical_date }}"
next_logical_date = "{{ next_execution_date }}"

# Loop through pumps to create tasks

for pump_model in pumps:
    task_identifier = pump_model["model"].replace("_", "-")

    run_pumps_command = f"""
      {clone_repo_cmd} &&
      export PYTHONPATH="$CI_PROJECT_DIR/orchestration/:$PYTHONPATH" &&
      python3 /analytics/pump/pumps.py \
        --model={pump_model["model"]} \
        --sensitive={pump_model["sensitive"]} \
        --timestamp={pump_model["timestamp_column"]} \
        --inc_start={logical_date} \
        --inc_end={next_logical_date} \
        --stage={pump_model["stage"]} \
        --single={pump_model["single"]}
        """

    run_pumps = KubernetesPodOperator(
        **gitlab_defaults,
        image=DATA_IMAGE,
        task_id=task_identifier,
        name=task_identifier,
        secrets=[
            SNOWFLAKE_USER,
            SNOWFLAKE_PASSWORD,
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_LOAD_DATABASE,
            SNOWFLAKE_LOAD_WAREHOUSE,
        ],
        env_vars=pod_env_vars,
        affinity=get_affinity("extraction"),
        tolerations=get_toleration("extraction"),
        arguments=[run_pumps_command],
        dag=dag,
    )
