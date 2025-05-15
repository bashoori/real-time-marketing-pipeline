# 📈 Real-Time Marketing Analytics Pipeline for E-Commerce Campaigns

This project simulates a real-time marketing analytics pipeline for tracking ad performance metrics like CTR (Click-Through Rate), impressions, and conversions from sources such as Google Ads, Instagram, and email campaigns.

---

## 📊 Architecture Overview

![Architecture Diagram](https://github.com/bashoori/repo/blob/master/real-time-marketing-pipeline/image1.png)

---

## 🚀 Features

- Real-time ingestion with **Amazon Kinesis**
- Batch processing with **Apache Airflow**
- Transformation using **Python**
- Storage in **Amazon Redshift**
- Alerts via **AWS Lambda** + **SNS**
- Dockerized local development
- Monitored with **CloudWatch**

---

## 🛠️ Tools & Technologies

| Category       | Tools Used                                                 |
|----------------|------------------------------------------------------------|
| Programming    | Python, SQL                                                |
| Cloud Services | AWS (S3, Redshift, Lambda, Kinesis, SNS, CloudWatch)       |
| Orchestration  | Apache Airflow                                             |
| Containerization | Docker                                                   |
| Monitoring     | CloudWatch, PyTest                                         |
| CI/CD          | GitHub Actions                                             |

---

## 📂 Project Structure

```bash
real-time-marketing-pipeline/

├── airflow/                   
│   ├── dags/
│   │   └── marketing_kpi_dag.py
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── airflow.cfg (optional)
├── scripts/
│   ├── ingest_ads_api.py
│   └── transform_metrics.py
├── sql/
│   └── create_tables.sql
│   └── kpi_metrics.sql
├── tests/
│   └── test_transformations.py
├── .github/workflows/
│   └── main.yml
├── images/
│   └── architecture.png
├── README.md
└── requirements.txt
