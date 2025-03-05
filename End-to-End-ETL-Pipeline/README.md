# End-to-End ETL Pipeline with Python, Airflow, Spark, Docker, S3, Snowflake & Google Looker Studio

## Introduction
Welcome to this project on building an end-to-end ETL pipeline using Python, Apache Airflow, Spark, Docker, S3, Snowflake, and Google Looker Studio.
In this project, I’ll walk you through the complete process of extracting, transforming, and
visualizing data from YouTube API, all automated with Apache Airflow and deployed in a
Dockerized environment.

## Architecture

![Project Architecture](Project_Architecture.png)

## step 1: Obtain a Youtube Data API Key

- Visit the Google Developers Console.
- Create a new project.
- Search for the “YouTube Data API” and enable it.
- Generate new credentials and copy the API key for later use in the project.

  
![Youtube API](Google_API.png)


## step 2: Acquire AWS Access Key ID and Secret Access Key

- Log in to your [AWS Management Console](https://aws.amazon.com/console/).
- Navigate to the IAM (Identity and Access Management) section and create a new user.
- Attach the necessary policies for S3 access and create Access Keys.
- Save the generated Access Key ID and Secret Access Key securely for use in the project.


![Youtube API](AWS_Access_Key.png)

## step 3: Using VS code Create a Docker Image

- Create a new folder for your project and name it as “Airflow-Project”
- All code share in below project

 [Airflow-Project](Airflow-Project)

The process starts with extracting trending video data from YouTube using the YouTube
API. This includes information like video titles, views, likes, comments, and categories.

## step 4: Run the docker

Run the compose up to run the docker.

![Docker Image](Docker_Image.png)


## step 5: Open the Airflow DAG

Trigger the youtube_etl_dag and run the process

![Airflow](Airflow_ETL_Dag.png)

## Step 6: Open AWS s3 bucket

After run the DAG successfully the YouTube Data available in S3 bucket.

![Amazon_S3_Bucket](Amazon_S3_Bucket.png)

## Step 7: connect S3 to Snowflake database

Run the the query [Snowflake Query](Snowflake_Query.html) 

![Snowflake](snowflake_query.png)


