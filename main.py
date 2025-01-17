from dotenv import load_dotenv
from dags.etl import get_json_data, load_table_from_json
from dags.db import new_biquery_client


def main():
    # db_client = new_biquery_client()
    # data = get_json_data()
    # load_table_from_json(db_client, "stops", data)
    print("Running Pipeline")


if __name__ == "__main__":
    load_dotenv()
    main()
