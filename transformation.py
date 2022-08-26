from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import desc, lit
from pyspark.sql.types import DateType
import re
from datetime import datetime


def transform(task_instance):
    spark = SparkSession.builder.appName("reddit post's pipeline").getOrCreate()

    objects = task_instance.xcom_pull(task_ids="upload_to_storage", key="return_value")

    stop_words = spark.read.text("gs://reddit-posts2/stop_words.txt")

    for object in objects:
        bucket_name = "reddit-posts2"
        subreddit = object[0]
        paths = object[1]
        date = paths[0].split(" ")[1].split(".")[0]
        date = datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
        list_of_paths = ""
        for path in paths:
            list_of_paths += f"gs://{bucket_name}/{path},"
        list_of_paths = list_of_paths[:-1]

        paths = map(lambda s: "gs://" + bucket_name + "/" + s, paths)
        df = spark.read.text(paths)
        rdd = df.rdd
        rdd = rdd.map(lambda s: s["value"])
        rdd = rdd.flatMap(lambda s: s.split(', "'))

        matches = ['body"', 'title": "', 'selftext"']
        rdd = rdd.filter(
            lambda s: any(x in s for x in matches)
        )  # filter the tags I don't need

        rdd = rdd.map(
            lambda s: s.replace('body":', "")
            .replace('selftext":', "")
            .replace('title":', "")
        )

        rdd = rdd.map(lambda s: s.encode().decode("raw_unicode_escape"))

        rdd = rdd.filter(
            lambda s: "\\n&gt;" not in s
        )  # remove all quotes, including the bot that quotes articles
        rdd = rdd.map(
            lambda s: re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", s) 
        ) # filter URLs
        rdd = rdd.map(
            lambda s: s.replace("\\n", " ").replace("&gt", " ").replace("&amp;#32;", " ")
        )  # removing other wierd formatting characters
        rdd = rdd.map(
            lambda s: re.sub("\W+", " ", s)
        )  # remove non-alphanumeric characters, save for blank space

        a, b = "áéíóúü", "aeiouu"
        trans = str.maketrans(a, b)
        rdd = rdd.map(lambda s: s.translate(trans))  # remove tilde: á -> a, é -> e ...
        rdd = rdd.map(lambda s: s.lower())
        rdd = rdd.flatMap(lambda s: s.split(" "))
        rdd = rdd.filter(lambda s: s != "")

        row = Row("word")
        df = rdd.map(row).toDF()

        df = df.join(stop_words, df.word == stop_words.value, how="left_anti")
        df = df.groupBy(df["word"]).count().sort(desc("count"))
        df = df.filter("count > 5")
        df = df.withColumn("subreddit", lit(subreddit))
        df = df.withColumn("date", lit(date).cast(DateType()))

        df.show(n=30, truncate=False)

        df.write.format("bigquery").option("writeMethod", "direct").mode("append").save(
           "reddit_dataset.words"
        )


