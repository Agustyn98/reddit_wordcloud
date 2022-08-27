FROM ubuntu:22.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         python3-pip default-jre  \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV AIRFLOW_HOME=/airflow


# Python dependencies
RUN pip install --no-cache-dir --upgrade pyspark && \
    pip install --no-cache-dir google-cloud-storage &&\
    pip install --no-cache-dir "apache-airflow==2.3.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.10.txt"


# Spark dependencies (jars)
COPY spark_dependencies/* /usr/local/lib/python3.10/dist-packages/pyspark/jars/

COPY pipeline.py transformation.py functions.py /airflow/dags/

# Service account key
COPY gcp_key.json ~/gcp_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=~/gcp_key.json

# Set timezone
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/Argentina/Mendoza" apt-get install -y tzdata
