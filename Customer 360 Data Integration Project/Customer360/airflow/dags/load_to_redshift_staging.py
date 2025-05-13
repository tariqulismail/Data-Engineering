# /dags/load_to_redshift_staging.py
from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define S3 bucket and Redshift connection
S3_BUCKET = 'customer-360-raw-data'
REDSHIFT_CONN_ID = 'redshift_default'

# Create DAG
dag = DAG(
    'load_to_redshift_staging',
    default_args=default_args,
    description='Load data from S3 to Redshift staging',
    schedule=timedelta(days=1),
    catchup=False
)

# Load CRM data to Redshift
load_crm_to_redshift = S3ToRedshiftOperator(
    task_id='load_crm_to_redshift',
    schema='STAGING',
    table='crm_customers',
    s3_bucket=S3_BUCKET,
    s3_key='raw/{{ds}}/crm/crm_data.csv',
    copy_options=['CSV', 'IGNOREHEADER 1'],
    aws_conn_id='aws_default',
    redshift_conn_id=REDSHIFT_CONN_ID,
    dag=dag
)

# Load Salesforce data to Redshift
load_salesforce_to_redshift = S3ToRedshiftOperator(
    task_id='load_salesforce_to_redshift',
    schema='STAGING',
    table='salesforce_contacts',
    s3_bucket=S3_BUCKET,
    s3_key='raw/{{ds}}/salesforce/salesforce_contacts.csv',
    copy_options=['CSV', 'IGNOREHEADER 1'],
    aws_conn_id='aws_default',
    redshift_conn_id=REDSHIFT_CONN_ID,
    dag=dag
)

# Load Google Analytics data to Redshift
load_ga_to_redshift = S3ToRedshiftOperator(
    task_id='load_ga_to_redshift',
    schema='STAGING',
    table='ga_sessions',
    s3_bucket=S3_BUCKET,
    s3_key='raw/{{ds}}/google_analytics/ga_sessions.csv',
    copy_options=['CSV', 'IGNOREHEADER 1'],
    aws_conn_id='aws_default',
    redshift_conn_id=REDSHIFT_CONN_ID,
    dag=dag
)

# Load Transaction data to Redshift
load_transactions_to_redshift = S3ToRedshiftOperator(
    task_id='load_transactions_to_redshift',
    schema='STAGING',
    table='offline_transactions',
    s3_bucket=S3_BUCKET,
    s3_key='raw/{{ds}}/transactions/offline_transactions.csv',
    copy_options=['CSV', 'IGNOREHEADER 1'],
    aws_conn_id='aws_default',
    redshift_conn_id=REDSHIFT_CONN_ID,
    dag=dag
)