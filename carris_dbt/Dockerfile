FROM --platform=linux/amd64 ghcr.io/dbt-labs/dbt-bigquery:latest

# Define dbt profiles directory
ENV DBT_PROFILES_DIR=/root/.dbt

# Create dbt profiles directory
RUN mkdir -p /root/.dbt

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
