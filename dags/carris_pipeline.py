from airflow.decorators import dag, task
from datetime import datetime, timedelta

from pipeline.etl import get_json_data, load_table_from_json
from bigquery.client import new_biquery_client

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="carris_pipeline",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    description="A pipeline to extract and load data from Carris API",
    start_date=datetime.datetime(2025, 1, 16),
    catchup=False,
)
def carris_pipeline():
    @task
    def extract():
        return get_json_data()

    @task
    def load_into_database(db_client, data, table_name):
        return load_table_from_json(
            db_client=db_client, table_name=table_name, data=data
        )

    data = extract()
    db_client = new_biquery_client()
    load_into_database(db_client, data, "stops")


etl_dag = carris_pipeline()
