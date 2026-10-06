import os
from datetime import datetime
from airflow.sdk import DAG
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import ExecutionMode, LoadMode
from docker.types import Mount

DBT_PARSE_PATH = "/opt/airflow/dbt"
DBT_RUNTIME_PATH = "/usr/app/dbt"
DBT_HOST_PATH = os.environ["DBT_HOST_PROJECT_DIR"]

with DAG(dag_id="dbt_silver", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["dbt", "cosmos", "silver"]) as dag:
    DbtTaskGroup(
        group_id="silver",
        project_config=ProjectConfig(dbt_project_path=DBT_PARSE_PATH),
        profile_config=ProfileConfig(profile_name="lakehouse", target_name="dev", profiles_yml_filepath=f"{DBT_PARSE_PATH}/profiles.yml"),
        execution_config=ExecutionConfig(execution_mode=ExecutionMode.DOCKER),
        render_config=RenderConfig(load_method=LoadMode.MANIFEST, select=["path:models/silver"]),
        operator_args={
            "image": "bank-dbt:dev",
            "docker_url": "unix://var/run/docker.sock",
            "network_mode": "airflow-development",
            "mount_tmp_dir": False,
            "auto_remove": "success",
            "working_dir": DBT_RUNTIME_PATH,
            "mounts": [
                Mount(source=DBT_HOST_PATH, target=DBT_RUNTIME_PATH, type="bind"),
                Mount(source="/home/support/airflow/cert", target="/opt/dbt/certs", type="bind", read_only=True),
            ],
            "environment": {
                "DBT_PROFILES_DIR": DBT_RUNTIME_PATH,
                "DBT_LIVY_HOST": os.environ.get("DBT_LIVY_HOST", ""),
                "DBT_LIVY_USER": os.environ.get("DBT_LIVY_USER", ""),
                "DBT_LIVY_PASSWORD": os.environ.get("DBT_LIVY_PASSWORD", ""),
            },
        },
    )
