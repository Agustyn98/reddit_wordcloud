FROM apache/airflow:2.3.4
USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         python3-pip python3-venv default-jre  \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

#go back to a normal user after installation is complete
USER airflow

# Python dependencies
RUN pip install --no-cache-dir --upgrade pyspark && \
    pip install --no-cache-dir google-cloud-storage 

# Spark dependencies (jars)
COPY spark_dependencies/* /usr/local/lib/python3.9/dist-packages/pyspark/jars/
COPY --chown=airflow:root pipeline.py transformation.py functions.py stop_words.txt /opt/airflow/dags/

# Service account key
COPY gcp_key.json ~/gcp_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=~/gcp_key.json

