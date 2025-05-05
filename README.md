# ELT Pipeline for Public Transportation Information

This project implements a simplified ELT pipeline to **extract** data from the [Carris API](https://github.com/carrismetropolitana/api) and **load** it into **BigQuery** for testing purposes. The pipeline is orchestrated using **Apache Airflow** and designed as a solution to test and experiment with Airflow DAGs and scheduling.

The project is built using Docker Compose and integrates the following technologies:

- **Carris API**: Data source for public transportation information in the Lisbon Metropolitan area.
- **Apache Airflow**: Orchestration of the ELT pipeline.
- **BigQuery**: Destination for loading and analyzing data.

## Project Structure
```
.
├── dags
│   ├── carris_pipeline.py          # Main Airflow DAG file
│   ├── libs
│   │   ├── etl.py                  # Custom extraction and loading functions
│   │   └── db.py                   # Custom database functions for Bigquery
└── docker-compose.yml              # Docker Compose configuration
```

## Setup Local Environment
### Set up Docker Compose
Ensure that you have Docker and Docker Compose installed. This project uses Docker Compose to set up the required services, including Airflow and dbt.

Run the following command to start the services:
```bash
docker-compose up --build
```

This will:
- Start Airflow (Webserver, Scheduler, and Worker).
- Start a dbt container for running transformations.
- Make the Carris API extraction tasks run on a daily basis.


### Start the Airflow Web UI
Once the containers are up, you can access the Airflow web interface by navigating to http://localhost:8080.

Login wiht the default credentials:
- **Username**: airflow
- **Password**: airflow

You will be able to monitor the execution of the pipeline, review logs, and manage the DAG.

## DAG Overview
- **Extraction of Carris Data**

JSON data is fetched from the Carris API for various endpoints (vehicles, lines, stops, etc.).
GZIP compressed data (GTFS format) is also extracted and loaded.

- **Loading into BigQuery**

Data is loaded into BigQuery into a schema named raw.

- **Scheduling**

The DAG runs daily, pulling the latest data from the Carris API, transforming it, and loading it into BigQuery.