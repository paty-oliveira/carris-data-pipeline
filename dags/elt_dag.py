import os
from datetime import datetime, timedelta

from airflow.decorators import task, dag
from libs.pipeline import extract_json_data_and_load, extract_zip_files_and_load


ENDPOINT = "https://api.carrismetropolitana.pt/v1"
DATABASE_SCHEMA = "raw"
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


@task(task_id="extract_and_load_carris_data")
def extract_and_load_carris_json_data():
    params = ["vehicles", "lines", "stops", "alerts", "municipalities", "routes"]

    return extract_json_data_and_load(ENDPOINT, params, DATABASE_SCHEMA)


@task(task_id="extract_and_load_carris_gzip_data")
def extract_and_load_carris_gzip_data():
    param = "gtfs"

    return extract_zip_files_and_load(ENDPOINT, param, DATABASE_SCHEMA)


@task.bash(task_id="transform_carris_data")
def transform_carris_data():
    return f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir ."


@dag(
    dag_id="carris_pipeline",
    default_args=default_args,
    description="A simple pipeline for loading Carris data into BigQuery",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 1, 20),
    tags=["carris", "pipeline"],
    catchup=False,
)
def carris_pipeline():
    extract_and_load_json_data = extract_and_load_carris_json_data()
    extract_and_load_gzip_data = extract_and_load_carris_gzip_data()
    transform_data = transform_carris_data()

    [extract_and_load_json_data, extract_and_load_gzip_data] >> transform_data


carris_pipeline()
