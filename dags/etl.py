import requests
from db import new_biquery_client
from zipfile import ZipFile
from io import BytesIO
import os
import pandas as pd


def get_json_data(endpoint, param):
    try:
        response = requests.get(endpoint + param)

        if response.ok:
            data = response.json()
            print(f"Data from {param} endpoint was fetched")

            return data
    except Exception as error:
        print(f"Error in API call - {error}")


def download_zip_files(endpoint, param, output_dir):
    try:
        response = requests.get(endpoint + param, stream=True)

        if response.ok:
            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(output_dir)
                print(f"Extracted {len(zip_file.namelist())} files from zip")

    except Exception as error:
        print(f"Error in downloading zip file - {error}")


def extract_json_data_and_load(endpoint, params, database_schema):
    db_client = new_biquery_client()

    try:
        for param in params:
            data = get_json_data(endpoint, param)
            table_name = f"{database_schema}.{param}"
            db_client.load_table_from_json(data, destination=table_name)
            print(f"Created and loaded table: {table_name} with {len(data)} rows")

    except Exception as error:
        print(f"Error during loading data in db - {error}")


def extract_zip_files_and_load(
    endpoint, param, database_schema, output_dir="tmp_files"
):
    db_client = new_biquery_client()

    os.makedirs(output_dir, exist_ok=True)
    try:
        download_zip_files(endpoint, param, output_dir)
        os.chdir(output_dir)

        for file_name in os.listdir():
            if file_name.endswith(".txt"):
                file_path = os.path.abspath(file_name)
                data = pd.read_csv(file_path, low_memory=False)
                table_name = file_name.split(".")[0]
                full_table_name = f"{database_schema}.archive_{table_name}"

                if not data.empty:
                    db_client.load_table_from_dataframe(
                        data, destination=full_table_name
                    )
                    print(
                        f"Created and loaded table: {table_name} with {len(data)} rows"
                    )
                else:
                    print(f"Empty table: {table_name}")
            else:
                print(f"File {file_name} is not an expected file")

    except Exception as error:
        print(f"Error during loading data in db - {error}")
