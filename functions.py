import requests
import json
from datetime import datetime
import os
from google.cloud import storage


def get_top_posts(urls={}):
    top_posts = []
    for url in urls:
        response = requests.get(urls[url], headers={"User-agent": "Not_a_Bot_941"})
        content = response.text

        top_posts.append((url, content))

    subreddit_and_links = []
    for posts in top_posts:
        links = get_links_from_subreddit(posts[1])
        subreddit_and_links.append((posts[0], links))

    return subreddit_and_links


def get_links_from_subreddit(post):
    links = []
    data = json.loads(post)  # dictionary
    for child in data["data"]["children"]:
        link = child["data"]["permalink"]
        links.append(link)

    return links


def get_posts(task_instance):
    subreddits_and_links = task_instance.xcom_pull(
        task_ids="get_links", key="return_value"
    )
    subreddit_and_files = []
    for sub in subreddits_and_links:
        for link in sub[1]:
            response = requests.get(
                "https://www.reddit.com" + link + ".json",
                headers={"User-agent": "beepBoop123"},
            )
            content = response.text
            dt = datetime.now()
            timestamp = str(datetime.timestamp(dt))
            filename = "/tmp/" + sub[0] + " " + timestamp + ".json"

            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(content)

            subreddit_and_files.append((sub[0], filename))

    return subreddit_and_files


def upload_files(task_instance):
    files = task_instance.xcom_pull(task_ids="get_files", key="return_value")

    subreddit_and_object = []
    objects = []
    last_subreddit = None

    for file in files:
        bucket_name = "reddit-posts2"
        filepath = file[1]
        subreddit_name = file[0]

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        object_path = "datalake/" + subreddit_name + "/" + filepath[5:]

        if last_subreddit != subreddit_name and last_subreddit is not None:
            subreddit_and_object.append([last_subreddit, objects.copy()])
            objects.clear()

        last_subreddit = subreddit_name
        objects.append(object_path)
        blob = bucket.blob(object_path)
        blob.upload_from_filename(filepath)

    subreddit_and_object.append([last_subreddit, objects])

    return subreddit_and_object
