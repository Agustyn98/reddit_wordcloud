from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from transformation import transform
from functions import get_top_posts, get_posts, upload_files


num_posts = "30"
urls = {
    "argentina": "https://www.reddit.com/r/argentina/top/.json?limit=" + num_posts,
    # "RepublicaArgentina": "https://www.reddit.com/r/RepublicaArgentina/top/.json?limit="
    # + num_posts,
    "Republica_Argentina": "https://www.reddit.com/r/Republica_Argentina/top/.json?limit="
    + num_posts,
    # "ArgentinaBenderStyle": "https://www.reddit.com/r/ArgentinaBenderStyle/top/.json?limit="
    # + num_posts,
    "dankgentina": "https://www.reddit.com/r/dankgentina/top/.json?limit=" + num_posts,
    # "BasedArgentina": "https://www.reddit.com/r/BasedArgentina/top/.json?limit="
    # + num_posts,
    "Argaming": "https://www.reddit.com/r/Argaming/top/.json?limit=" + num_posts,
    "merval": "https://www.reddit.com/r/merval/top/.json?limit=" + num_posts,
}

with DAG(
    "reddit_pipeline",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="get_links", python_callable=get_top_posts, op_kwargs={"urls": urls}
    )

    t2 = PythonOperator(task_id="get_files", python_callable=get_posts)

    t3 = PythonOperator(task_id="upload_to_storage", python_callable=upload_files)

    t4 = PythonOperator(task_id="transformation", python_callable=transform)

    t1 >> t2 >> t3 >> t4
