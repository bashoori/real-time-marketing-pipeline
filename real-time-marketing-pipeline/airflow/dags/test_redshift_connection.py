from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import os
import logging


def test_redshift_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("REDSHIFT_DB"),
            user=os.getenv("REDSHIFT_USER"),
            password=os.getenv("REDSHIFT_PASSWORD"),
            host=os.getenv("REDSHIFT_HOST"),
            port=os.getenv("REDSHIFT_PORT", 5439)
        )
        cursor = conn.cursor()
        cursor.execute("SELECT current_date;")
        result = cursor.fetchone()
        logging.info(f"✅ Successfully connected to Redshift. Current date: {result[0]}")

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("❌ Failed to connect to Redshift", exc_info=True)
        raise


with DAG(
    dag_id="test_redshift_connection",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["test", "redshift"]
) as dag:
    run_test = PythonOperator(
        task_id="run_redshift_test",
        python_callable=test_redshift_connection
    )