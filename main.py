from dotenv import load_dotenv
from etl import get_json_data, load_table_from_json
from bigquery import new_biquery_client


def main():
    endpoint = "https://api.carrismetropolitana.pt/"
    db_client = new_biquery_client()

    municipalities_param = "municipalities"
    municipalities_data = get_json_data(endpoint=endpoint + municipalities_param)
    load_table_from_json(db_client, municipalities_param, municipalities_data)


if __name__ == "__main__":
    load_dotenv()
    main()
