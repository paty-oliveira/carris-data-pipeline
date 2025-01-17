import os
from google.oauth2 import service_account
from google.cloud import bigquery

CREDENTIALS_PATH = os.getenv("SERVICE_ACCOUNT_FILE")


def new_biquery_client():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH
    )

    return bigquery.Client(credentials=credentials)
