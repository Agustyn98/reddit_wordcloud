# Word cloud for Reddit
Visual free form text representation of single words, grouped by subreddit and date

## About this project:
This project is a data pipeline that scraps the top posts of any number of subreddits, filters and aggregates words in titles, descriptions and comments, and finally loads the data into BigQuery.

### Built With:

- Data Ingestion: Python running on Airflow
- Workflow orchestration: Airflow
- Data Lake: Google Cloud Storage
- Data Warehouse: BigQuery
- Batch Processing: PySpark
- Visualization: Data Studio

![new_diagram](https://user-images.githubusercontent.com/66125885/187461650-b954c88d-3cc6-4ef9-9746-9df777e3999e.jpeg)



## Results and live dashboard

- Examples
    - /r/argentina, 29-08-2022
    ![Screenshot_2022-08-30_11-08-01](https://user-images.githubusercontent.com/66125885/187459857-b189b0e1-d7eb-4c3c-8e3c-e973bd4bcb77.png)

    - /r/argaming week from 29-08-2022 to 05-08-2022
        - *picture*

### Live dashboard
[Live Dashboard on Data Studio](https://datastudio.google.com/reporting/2f43e030-9bdb-4a70-a9b3-f0ec6d3c270b)

## Instructions:

### Prerequesites:
- Terraform
- Docker
- A Google Cloud Platform account

### Create a Google Cloud project
1. Go to Google Cloud and create a new project.
2. Go to IAM and create a Service Account with these roles:
    BigQuery Admin,
    Storage Admin

3. Download the service account credentials and rename it to gcp_key.json


### Set up the infrastructure on Google Cloud:
1. Open resources.tf and modify the project name.
2. Set up authentication by running 
```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp_key.json
``` 
3. Create the resources
```
terraform init
```
```
terraform apply
```

### Running with Docker:

1. Copy service account key to this repo's main folder
2. ```docker build -t reddit_app .```
3. ```docker run -it -p 8080:8080 airflow standalone```
4. Go to localhost:8080 and use the username and password that appear on the terminal to log into airflow
4. Run the pipeline from the UI at localhost:8080

