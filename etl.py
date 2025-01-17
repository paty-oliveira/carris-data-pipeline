import os
import requests

DATASET_ID = os.getenv("DATASET_ID")


def get_json_data(endpoint):
    try:
        response = requests.get(endpoint)

        if response.ok:
            data = response.json()
            print(f"Data from {endpoint} endpoint was fetched")

            return data
    except Exception as error:
        print(f"Error in API call - {error}")


def load_table_from_json(db_client, table_name, data):
    try:
        db_client.load_table_from_json(data, destination=f"{DATASET_ID}.{table_name}")
        print(f"Created and loaded table: {table_name} with {len(data)} rows")

    except Exception as error:
        print(f"Error during loading data in db - {error}")
