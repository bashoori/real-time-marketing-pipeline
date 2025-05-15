from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3
import pandas as pd
import os
import logging
import psycopg2


# === DAG Default Arguments ===
default_args = {
    'owner': 'bita',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# === DAG Setup ===
with DAG(
    dag_id='marketing_kpi_dag',
    default_args=default_args,
    description='Extract marketing data from S3, transform it, and load to Redshift',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['marketing', 'ETL', 'S3', 'Redshift']
) as dag:

    def extract_from_s3():
        """Download sample CSV file from S3"""
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        bucket = 'realtime-marketing-data'
        key = 'raw/google_ads/sample.csv'
        local_path = '/tmp/sample.csv'

        s3 = boto3.client('s3', region_name=region)
        logging.info(f"Downloading s3://{bucket}/{key} to {local_path}")
        s3.download_file(bucket, key, local_path)

    def transform_campaign_data():
        """Calculate CTR and save transformed data"""
        input_path = '/tmp/sample.csv'
        output_path = '/tmp/transformed.csv'

        df = pd.read_csv(input_path)
        df['CTR'] = df['clicks'] / df['impressions']
        df.to_csv(output_path, index=False)

        logging.info(f"Transformed data saved to {output_path}")

    def load_to_redshift():
        """Load transformed data into Redshift"""
        conn = psycopg2.connect(
            dbname=os.getenv("REDSHIFT_DB"),
            user=os.getenv("REDSHIFT_USER"),
            password=os.getenv("REDSHIFT_PASSWORD"),
            host=os.getenv("REDSHIFT_HOST"),
            port=os.getenv("REDSHIFT_PORT", 5439)
            
        )

        cursor = conn.cursor()
        with open('/tmp/transformed.csv', 'r') as f:
            next(f)  # Skip header
            cursor.copy_expert("COPY campaign_metrics FROM STDIN WITH CSV", f)
            conn.commit()

        cursor.close()
        conn.close()
        logging.info("Data successfully loaded into Redshift")

    # === Task Definitions ===
    t1 = PythonOperator(
        task_id='extract_from_s3',
        python_callable=extract_from_s3
    )

    t2 = PythonOperator(
        task_id='transform_campaign_data',
        python_callable=transform_campaign_data
    )

    t3 = PythonOperator(
        task_id='load_to_redshift',
        python_callable=load_to_redshift
    )

    # === DAG Flow ===
    t1 >> t2 >> t3