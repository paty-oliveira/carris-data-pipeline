import requests
from dotenv import load_dotenv
import os


def get_json_data(endpoint):
    try:
        response = requests.get(endpoint)

        if response.ok:
            data = response.json()
            print(f"Data from {endpoint} endpoint was fetched")

            return data
    except Exception as error:
        print(f"Error in API call - {error}")


def main():
    endpoint = "https://api.carrismetropolitana.pt/"

    vehicles_data = get_json_data(endpoint=endpoint + "vehicles")
    print(vehicles_data)

    municipalities_data = get_json_data(endpoint=endpoint + "municipalities")
    print(municipalities_data)


if __name__ == "__main__":
    load_dotenv()
    main()
