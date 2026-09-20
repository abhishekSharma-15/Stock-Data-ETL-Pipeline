"""
Airflow Dag Logic.

Responsibilities:
- Schedule and orchestrate the Stock ETL Pipeline
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append('/opt/airflow/stock_pipeline')

from src.pipeline.etl_pipeline import StockETLPipeline
from src.utils.config import STOCK_SYMBOLS

def run_pipeline(symbol):
    pipeline = StockETLPipeline(symbol)
    pipeline.run()

default_args= {
    'owner': 'abhishek',
    'start_date': datetime(2025,1,1),
    'retries': 1
}

with DAG(
    dag_id = 'stock_etl_pipeline',
    schedule_interval = '@daily',
    default_args = default_args,
    catchup= False
) as dag:

    tasks = []

    for symbol in  STOCK_SYMBOLS:
        task = PythonOperator(
            task_id = f'etl_{symbol.lower()}',
            python_callable = run_pipeline,
            op_args =[symbol]
        )
        tasks.append(task)  