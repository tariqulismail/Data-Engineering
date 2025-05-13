# /dags/dbt_transform.py
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
import os

# Define paths
DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = DBT_PROJECT_DIR

# Environment variables for dbt (can also be set in Airflow UI)
os.environ["REDSHIFT_USER"] = "your_redshift_username"  # Use Airflow secrets in production
os.environ["REDSHIFT_PASSWORD"] = "your_redshift_password"  # Use Airflow secrets in production

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'dbt_transform',
    default_args=default_args,
    description='Transform data using dbt and load to final tables',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Wait for the staging data to be loaded
wait_for_staging = ExternalTaskSensor(
    task_id='wait_for_staging_data',
    external_dag_id='load_to_redshift_staging',  # The DAG that loads data to staging
    external_task_id=None,  # None means wait for the entire DAG to complete
    timeout=3600,
    mode='reschedule',
    dag=dag
)

# Run dbt deps to install dependencies
dbt_deps = BashOperator(
    task_id='dbt_deps',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt deps --profiles-dir {DBT_PROFILES_DIR}',
    dag=dag
)

# Run dbt to transform data and build staged models
dbt_run_staging = BashOperator(
    task_id='dbt_run_staging',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --models staging.* --profiles-dir {DBT_PROFILES_DIR}',
    dag=dag
)

# Run dbt to transform data and build final models in REPORTING schema
dbt_run_marts = BashOperator(
    task_id='dbt_run_marts',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --models marts.* --profiles-dir {DBT_PROFILES_DIR}',
    dag=dag
)

# Test the dbt models to ensure data quality
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --profiles-dir {DBT_PROFILES_DIR}',
    dag=dag
)

# Generate dbt documentation
dbt_docs_generate = BashOperator(
    task_id='dbt_docs_generate',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt docs generate --profiles-dir {DBT_PROFILES_DIR}',
    dag=dag
)

# Serve dbt documentation (optional, for local development)
# dbt_docs_serve = BashOperator(
#     task_id='dbt_docs_serve',
#     bash_command=f'cd {DBT_PROJECT_DIR} && dbt docs serve --profiles-dir {DBT_PROFILES_DIR} --port 8080',
#     dag=dag
# )

# Set the task dependencies
wait_for_staging >> dbt_deps >> dbt_run_staging >> dbt_run_marts >> dbt_test >> dbt_docs_generate