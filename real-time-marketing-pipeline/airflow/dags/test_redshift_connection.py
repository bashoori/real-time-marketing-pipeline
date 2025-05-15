from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import os
import logging
import socket


def test_redshift_connection():
    # Retrieve and validate environment variables
    redshift_config = {
        "dbname": os.getenv("REDSHIFT_DB"),
        "user": os.getenv("REDSHIFT_USER"),
        "password": os.getenv("REDSHIFT_PASSWORD"),
        "host": os.getenv("REDSHIFT_HOST"),
        "port": int(os.getenv("REDSHIFT_PORT", "5439")),
    }

    missing = [key for key, value in redshift_config.items() if not value]
    if missing:
        logging.error(f"❌ Missing required Redshift config: {', '.join(missing)}")
        raise ValueError("Missing Redshift connection environment variables.")

    # Resolve host to IP
    try:
        resolved_ip = socket.gethostbyname(redshift_config["host"])
        logging.info(f"🔍 Resolved host {redshift_config['host']} to IP {resolved_ip}")
    except Exception as e:
        logging.error(f"❌ DNS resolution failed for host: {redshift_config['host']}", exc_info=True)
        raise

    # Attempt Redshift connection
    try:
        conn = psycopg2.connect(**redshift_config)
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
    tags=["test", "redshift"],
) as dag:

    run_test = PythonOperator(
        task_id="run_redshift_test",
        python_callable=test_redshift_connection
    )