Installation instructions:

1. create a virtual env
python -m venv reddit_pipeline

2. install the dependencies from requirements.txt

3. place the two .jar in lib/python3.10/pyspark/jars
these are spark's dependencies for gcs and bq

4. copy pipeline.py, functions.py transformation.py and stop_words.txt to wherever your DAGs folder is configured to be

5. Permissions: export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

5. run the dag from airflow's UI
