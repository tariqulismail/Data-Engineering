# /dags/customer_360_extract.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from datetime import datetime, timedelta
import sys
import os
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta


from simple_salesforce import Salesforce

import os

from google.cloud import bigquery
import google.cloud  # (not sufficient on its own)
from google.api_core.exceptions import GoogleAPIError


# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "personalfinancedata-33d6ed593671.json"



# Define base directory for output files
BASE_OUTPUT_DIR = '/opt/airflow/data/output'
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

# Generate CRM data function with explicit path
def generate_crm_data_with_path(num_records=1000):
    fake = Faker()
    Faker.seed(42)  # For reproducibility
    
    customers = []
    
    for i in range(1, num_records + 1):
        customer_id = f"CUST{i:06d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        
        # Generate signup dates within the last 3 years
        start_date = datetime.now() - timedelta(days=3*365)
        signup_date = fake.date_time_between(start_date=start_date, end_date='now')
        
        customers.append({
            'CustomerID': customer_id,
            'FirstName': first_name,
            'LastName': last_name,
            'Email': email,
            'Phone': phone,
            'SignupDate': signup_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(customers)
    output_path = os.path.join(BASE_OUTPUT_DIR, 'crm_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"CRM data saved to: {output_path}")
    return output_path

# Define similar functions for other data sources with explicit paths

# def generate_salesforce_data_with_path():
#     # Mock function since we don't have actual Salesforce credentials
#     fake = Faker()
#     Faker.seed(43)
    
#     contacts = []
#     for i in range(1, 1001):
#         salesforce_id = f"SF{i:08d}"
#         first_name = fake.first_name()
#         last_name = fake.last_name()
#         email = fake.email()
#         phone = fake.phone_number()
#         account_name = fake.company()
#         created_date = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
#         modified_date = fake.date_time_between(created_date).strftime('%Y-%m-%d %H:%M:%S')
        
#         contacts.append({
#             'SalesforceID': salesforce_id,
#             'FirstName': first_name,
#             'LastName': last_name,
#             'Email': email,
#             'Phone': phone,
#             'AccountName': account_name,
#             'CreatedDate': created_date,
#             'LastModifiedDate': modified_date
#         })
    
#     df = pd.DataFrame(contacts)
#     output_path = os.path.join(BASE_OUTPUT_DIR, 'salesforce_contacts.csv')
#     df.to_csv(output_path, index=False)
    
#     print(f"Salesforce data saved to: {output_path}")
#     return output_path

def connect_to_salesforce():
    sf = Salesforce(
        username='nasimbd80-mkkm@force.com',
        password='commando_00',
        security_token='RdqzcXtDUu7NFdDQbVQ8fGYS'
    )
    return sf

def generate_salesforce_data_with_path():
    
    sf = connect_to_salesforce()
        
    # Query Salesforce for Contact data
    query = """
    SELECT Id, FirstName, LastName, Email, Phone, Account.Name, 
           CreatedDate, LastModifiedDate
    FROM Contact
    LIMIT 1000
    """

    results = sf.query_all(query)
    records = results['records']
    
    # Transform Salesforce records into pandas DataFrame
    contacts = []
    for record in records:
        contact = {
            'SalesforceID': record['Id'],
            'FirstName': record['FirstName'],
            'LastName': record['LastName'],
            'Email': record['Email'],
            'Phone': record['Phone'],
            'AccountName': record['Account']['Name'],
            'CreatedDate': record['CreatedDate'],
            'LastModifiedDate': record['LastModifiedDate']
        }
        contacts.append(contact)
        
    df = pd.DataFrame(contacts)
    output_path = os.path.join(BASE_OUTPUT_DIR, 'salesforce_contacts.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Salesforce data saved to: {output_path}")
    return output_path



# Google Analytics data

# def generate_ga_data_with_path():
#     fake = Faker()
#     Faker.seed(44)
    
#     sessions = []
#     for i in range(1, 5001):
#         visitor_id = str(fake.random_number(digits=16))
#         visit_id = str(fake.random_number(digits=10))
#         date = fake.date_this_year().strftime('%Y%m%d')
#         pageviews = random.randint(1, 20)
#         time_on_site = random.randint(10, 1800)
#         device = random.choice(['mobile', 'desktop', 'tablet'])
#         country = fake.country()
#         source = random.choice(['google', 'direct', 'facebook', 'email', 'twitter'])
#         medium = random.choice(['organic', 'cpc', 'referral', 'email', 'social'])
        
#         # Generate a customer ID for some sessions
#         customer_id = f"CUST{random.randint(1, 1000):06d}" if random.random() > 0.3 else None
        
#         sessions.append({
#             'fullVisitorId': visitor_id,
#             'visitId': visit_id,
#             'date': date,
#             'pageviews': pageviews,
#             'timeOnSite': time_on_site,
#             'deviceCategory': device,
#             'country': country,
#             'source': source,
#             'medium': medium,
#             'CustomerID': customer_id
#         })
    
#     df = pd.DataFrame(sessions)
#     output_path = os.path.join(BASE_OUTPUT_DIR, 'ga_sessions.csv')
#     df.to_csv(output_path, index=False)
    
#     print(f"GA data saved to: {output_path}")
#     return output_path


# def generate_ga_data_with_path():

#     client = bigquery.Client()
    
#     # Query to get Google Analytics sample data
#     query = """
#     SELECT
#       fullVisitorId,
#       visitId,
#       date,
#       totals.pageviews,
#       totals.timeOnSite,
#       device.deviceCategory,
#       geoNetwork.country,
#       trafficSource.source,
#       trafficSource.medium
#     FROM
#       `bigquery-public-data.google_analytics_sample.ga_sessions_*`
#     WHERE
#       _TABLE_SUFFIX BETWEEN '20170101' AND '20170131'
#     LIMIT 5000
#     """
    
#     df = client.query(query).to_dataframe()
    
#     # Generate a simple customer mapping (in a real scenario, you'd match with actual customer IDs)
#     df['CustomerID'] = 'CUST' + df['fullVisitorId'].astype(str).str[-6:].str.zfill(6)
    
#     output_path = os.path.join(BASE_OUTPUT_DIR, 'ga_sessions.csv')
#     df.to_csv(output_path, index=False)
    
#     print(f"GA data saved to: {output_path}")
#     return output_path




def generate_ga_data_with_path():

        # Set Google Cloud credentials with absolute path
        #credentials_path = os.path.abspath("personalfinancedata-33d6ed593671.json")
        #print(f"Looking for credentials at: {credentials_path}")
        
        
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "personalfinancedata-33d6ed593671.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/dags/personalfinancedata-33d6ed593671.json"

        # Create BigQuery client
        print("Creating BigQuery client...")
        client = bigquery.Client()
        
        # Query to get Google Analytics sample data
        query = """
        SELECT
          fullVisitorId,
          visitId,
          date,
          totals.pageviews,
          totals.timeOnSite,
          device.deviceCategory,
          geoNetwork.country,
          trafficSource.source,
          trafficSource.medium
        FROM
          `bigquery-public-data.google_analytics_sample.ga_sessions_*`
        WHERE
          _TABLE_SUFFIX BETWEEN '20170101' AND '20170131'
        LIMIT 5000
        """
        
        print("Executing BigQuery query...")
        query_job = client.query(query)
        print(f"Query job created: {query_job.job_id}")
        
        print("Converting query results to DataFrame...")
        df = query_job.to_dataframe()
        print(f"DataFrame created with {len(df)} rows")
        
        # Generate a simple customer mapping
        print("Processing data...")
        df['CustomerID'] = 'CUST' + df['fullVisitorId'].astype(str).str[-6:].str.zfill(6)
        
        # Ensure output directory exists
        os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
        
        # Save to CSV
        output_path = os.path.join(BASE_OUTPUT_DIR, 'ga_sessions.csv')
        print(f"Saving data to: {output_path}")
        df.to_csv(output_path, index=False)
        
        print(f"GA data successfully saved to: {output_path}")
        return output_path


# Transaction data
def generate_transactions_with_path(num_customers=1000, min_transactions=1, max_transactions=10):
    fake = Faker()
    Faker.seed(45)
    
    transactions = []
    
    for i in range(1, num_customers + 1):
        customer_id = f"CUST{i:06d}"
        
        # Generate 1-10 transactions per customer
        num_transactions = random.randint(min_transactions, max_transactions)
        
        for j in range(num_transactions):
            transaction_id = f"TXN{len(transactions) + 1:08d}"
            
            # Generate transaction dates within the last year
            start_date = datetime.now() - timedelta(days=365)
            transaction_date = fake.date_time_between(start_date=start_date, end_date='now')
            
            # Generate random product and amount
            product_id = f"PROD{random.randint(1, 100):04d}"
            amount = round(random.uniform(10, 500), 2)
            
            # Generate random store location
            store_id = f"STORE{random.randint(1, 20):03d}"
            payment_method = random.choice(['CREDIT', 'DEBIT', 'CASH', 'MOBILE'])
            
            transactions.append({
                'TransactionID': transaction_id,
                'CustomerID': customer_id,
                'TransactionDate': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'ProductID': product_id,
                'Amount': amount,
                'StoreID': store_id,
                'PaymentMethod': payment_method
            })
    
    df = pd.DataFrame(transactions)
    output_path = os.path.join(BASE_OUTPUT_DIR, 'offline_transactions.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Transaction data saved to: {output_path}")
    return output_path

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define S3 bucket
S3_BUCKET = 'customer-360-raw-data'
S3_PREFIX = 'raw/{{ds}}'

# Create DAG
dag = DAG(
    'customer_360_extract',
    default_args=default_args,
    description='Extract data from multiple sources and load to S3',
    schedule=timedelta(days=1),
    catchup=False
)

# Task to generate CRM data
generate_crm_task = PythonOperator(
    task_id='generate_crm_data',
    python_callable=generate_crm_data_with_path,
    op_kwargs={'num_records': 1000},
    dag=dag
)

# Task to extract Salesforce data
extract_salesforce_task = PythonOperator(
    task_id='extract_salesforce_data',
    python_callable=generate_salesforce_data_with_path,
    dag=dag
)

# Task to extract Google Analytics data
extract_ga_task = PythonOperator(
    task_id='extract_ga_data',
    python_callable=generate_ga_data_with_path,
    dag=dag
)

# Task to generate transaction data
generate_transactions_task = PythonOperator(
    task_id='generate_transactions',
    python_callable=generate_transactions_with_path,
    dag=dag
)

# Tasks to upload data to S3
upload_crm_to_s3 = LocalFilesystemToS3Operator(
    task_id='upload_crm_to_s3',
    filename=f"{BASE_OUTPUT_DIR}/crm_data.csv",
    dest_bucket=S3_BUCKET,
    dest_key=f'{S3_PREFIX}/crm/crm_data.csv',
    replace=True,
    aws_conn_id='aws_default',  # Make sure this is configured
    dag=dag
)

upload_salesforce_to_s3 = LocalFilesystemToS3Operator(
    task_id='upload_salesforce_to_s3',
    filename=f"{BASE_OUTPUT_DIR}/salesforce_contacts.csv",
    dest_bucket=S3_BUCKET,
    dest_key=f'{S3_PREFIX}/salesforce/salesforce_contacts.csv',
    replace=True,
    aws_conn_id='aws_default',  # Make sure this is configured
    dag=dag
)

upload_ga_to_s3 = LocalFilesystemToS3Operator(
    task_id='upload_ga_to_s3',
    filename=f"{BASE_OUTPUT_DIR}/ga_sessions.csv",
    dest_bucket=S3_BUCKET,
    dest_key=f'{S3_PREFIX}/google_analytics/ga_sessions.csv',
    replace=True,
    aws_conn_id='aws_default',  # Make sure this is configured
    dag=dag
)

upload_transactions_to_s3 = LocalFilesystemToS3Operator(
    task_id='upload_transactions_to_s3',
    filename=f"{BASE_OUTPUT_DIR}/offline_transactions.csv",
    dest_bucket=S3_BUCKET,
    dest_key=f'{S3_PREFIX}/transactions/offline_transactions.csv',
    replace=True,
    aws_conn_id='aws_default',  # Make sure this is configured
    dag=dag
)

# Define task dependencies
generate_crm_task >> upload_crm_to_s3
extract_salesforce_task >> upload_salesforce_to_s3
generate_transactions_task >> upload_transactions_to_s3
extract_ga_task >> upload_ga_to_s3