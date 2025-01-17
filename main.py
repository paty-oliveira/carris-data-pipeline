import requests
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
from google.cloud import bigquery

CREDENTIALS_PATH = os.getenv("SERVICE_ACCOUNT_FILE")
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


def load_table_from_json(db_client, table_id, data):
    try:
        db_client.load_table_from_json(data, destination=table_id)
        print(f"Created and loaded table: {table_id} with {len(data)} rows")

    except Exception as error:
        print(f"Error during loading data in db - {error}")


def new_biquery_client():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH
    )

    return bigquery.Client(credentials=credentials)


def main():
    endpoint = "https://api.carrismetropolitana.pt/"
    db_client = new_biquery_client()

    municipalities_param = "municipalities"
    municipalities_data = get_json_data(endpoint=endpoint + municipalities_param)
    load_table_from_json(
        db_client, f"{DATASET_ID}.{municipalities_param}", municipalities_data
    )


if __name__ == "__main__":
    load_dotenv()
    main()
