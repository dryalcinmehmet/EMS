from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from psycopg2.extras import execute_values
import pandas as pd
import sqlalchemy as sql
import os
import sys
sys.path.append(os.getcwd())


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 4, 15),
    'email': ['example@email.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

conn_str   = 'mysql://root:-+@127.0.0.1/test'
dag = DAG('check_update_mysql',
          default_args=default_args,
          schedule_interval='@once',
          start_date=datetime(2017, 3, 20),
          catchup=False)

last_date_sql = ''
last_24 = ''
task1 = PythonOperator(task_id='connect_mysql',
                       provide_context=False,
                       python_callable=connect(),
                       dag=dag)

task2 = PythonOperator(task_id='select_mysql',
                       provide_context=False,
                       python_callable=select(),
                       dag=dag)

task1 >> task2

def connect(self):
    sql_engine = sql.create_engine(conn_str)

def select(self, **kwargs):
    qe = "select Date_Time from test2 order by Date_Time desc limit 1"
    last_date_sql = pd.read_sql_query(qe, sql_engine)['Date_Time'][0]
    task_instance = kwargs['task_instance']
    task_instance.xcom_push(key='last_date_sql', value=last_date_sql)
    task_instance.xcom_push(key='last_24', value=last_24)
    last_date_sql = task_instance.xcom_pull(task_ids='select_mysql', key='last_date_sql')
    last_24 = task_instance.xcom_pull(task_ids='select_mysql', key='last_24')








# df = pd.read_csv('export_dataframe.csv')
# df= df.sort_values(by=['Date_Time'])
# df.to_sql(name='test2', con=sql_engine, if_exists='append', index = False, chunksize=10000)

