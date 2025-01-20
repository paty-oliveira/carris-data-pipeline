# ELT Pipeline for Public Transportation Information

This project implements an ELT pipeline to extract data from the Carris API, transform it using dbt, and load it into BigQuery for analytics purposes. The pipeline is orchestrated using Apache Airflow, and dbt is used for transformation steps.\

This project is built using Docker Compose, and it integrates the following technologies:
- **Carris API**: [data source](https://github.com/carrismetropolitana/api) for public transportation information in the Lisbon Metropolitan area.
- **Apache Airflow**: for orchestration of the ETL pipeline.
- **dbt (Data Build Tool)**: for data transformation.
- **BigQuery**: for data storage and analysis.

## Project Structure
```
.
├── dags
│   ├── carris_pipeline.py          # Main Airflow DAG file
│   ├── libs
│   │   ├── etl.py                  # Custom extraction and loading functions
│   │   └── db.py                   # Custom database functions for Bigquery
├── dbt                             # dbt project directory
│   ├── dbt_project.yml             # dbt project configuration
│   ├── profiles.yml                # dbt profiles for BigQuery connection
│   ├── models                      # dbt models directory for transformations
│   └── ...
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

### Configure dbt profiles
Make sure to configure your profiles.yml file in the dbt directory with the correct credentials to connect to your BigQuery project.

Example of a BigQuery profile (profiles.yml):
```yml
your_project_name:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your_project_id
      dataset: your_dataset
      keyfile: /path/to/your/service_account_keyfile.json
      threads: 1
      timeout_seconds: 300

```
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

- **Transformation of raw data**

dbt is used to transform the raw data into structured and analyzable models.

- **Scheduling**

The DAG runs daily, pulling the latest data from the Carris API, transforming it, and loading it into BigQuery.