FROM apache/airflow:2.3.4
USER root
#WORKDIR "/reddit_app"

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         python3-pip python3-venv   \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#go back to a normal user after installation is complete
USER airflow

#RUN python3 -m venv airflow
#RUN . airflow/bin/activate
#ENV AIRFLOW_HOME=~/airflow

# CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.10.txt"
RUN pip install --no-cache-dir --upgrade pyspark && \
    pip install --no-cache-dir google-cloud-storage 
#    pip install --no-cache-dir "apache-airflow==2.3.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.10.txt"

#COPY spark_dependencies/* lib/python3.10/site-packages/pyspark/jars/
COPY spark_dependencies/* /usr/local/lib/python3.9/dist-packages/pyspark/jars/
#RUN mkdir ~/airflow
#RUN mkdir ~/airflow/dags
COPY --chown=airflow:root pipeline.py transformation.py functions.py stop_words.txt /opt/airflow/dags/

COPY gcp_key.json ~/gcp_key
ENV GOOGLE_APPLICATION_CREDENTIALS=~/gcp_key

