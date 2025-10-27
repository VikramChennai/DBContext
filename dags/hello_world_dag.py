from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define the function that will be called by the PythonOperator
def print_hello_world():
    """Simple function that prints Hello World to the logs."""
    print("Hello World")
    return "Hello World printed successfully!"

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='hello_world_dag',
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule_interval='@daily',  # Runs daily at midnight
    catchup=False,  # Don't run for past dates
    tags=['example', 'hello_world'],
)

# Define the task
print_hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello_world,
    dag=dag,
)

# Since there's only one task, no dependencies are needed
print_hello_task

