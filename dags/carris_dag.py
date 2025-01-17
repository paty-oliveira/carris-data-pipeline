from datetime import datetime, timedelta

from airflow.decorators import task, dag
from etl import extract_and_load


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


@task(task_id="extract_and_load_carris_data")
def extract_and_load_carris_data():
    endpoint = "https://api.carrismetropolitana.pt/"
    params = ["vehicles", "lines", "stops", "alerts", "municipalities", "routes"]
    database_schema = "raw"

    return extract_and_load(endpoint, params, database_schema)


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
    extract_and_load_carris_data()


carris_pipeline()
