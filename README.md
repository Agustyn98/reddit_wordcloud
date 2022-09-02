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

/r/argentina, 2022-09-02, right after the assasination attempt against the vice-president:

<img src="https://user-images.githubusercontent.com/66125885/188246702-ee1ad7db-1187-4994-a79d-1ccf95ba5e27.png" width=50% height=50%>

/r/argaming, 2022-08-31

<img src="https://user-images.githubusercontent.com/66125885/188246872-3cdc6f52-614a-4664-9c0a-269f0ec0c281.png" width=50% height=50%>


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

