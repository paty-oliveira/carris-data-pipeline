FROM --platform=linux/amd64 python:3.12-slim

# Run update and install git
RUN apt-get update && apt-get install -y \
  git \
  && apt-get clean

# Install dbt
RUN pip install dbt-core dbt-bigquery

# Create dbt profiles directory
RUN mkdir -p /root/.dbt

# Define dbt profiles directory
ENV DBT_PROFILES_DIR=/root/.dbt

# Copy profiles.yml to dbt profiles directory
COPY ./profiles.yml /root/.dbt/profiles.yml

# Copy dbt project to /opt/dbt
COPY . /opt/dbt/

# Set working directory
WORKDIR /opt/dbt/

# Install dbt dependencies
RUN dbt deps

# Run dbt debug
CMD ["dbt", "debug"]
