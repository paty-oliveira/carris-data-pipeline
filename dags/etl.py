import requests
from db import new_biquery_client


def get_json_data(endpoint, param):
    try:
        response = requests.get(endpoint + param)

        if response.ok:
            data = response.json()
            print(f"Data from {param} endpoint was fetched")

            return data
    except Exception as error:
        print(f"Error in API call - {error}")


def load_table_from_json(db_client, table_name, data):
    try:
        db_client.load_table_from_json(data, destination=table_name)
        print(f"Created and loaded table: {table_name} with {len(data)} rows")

    except Exception as error:
        print(f"Error during loading data in db - {error}")


def extract_and_load(endpoint, params, database_schema):
    db_client = new_biquery_client()

    for param in params:
        data = get_json_data(endpoint, param)
        load_table_from_json(
            db_client=db_client, table_name=f"{database_schema}.{param}", data=data
        )
