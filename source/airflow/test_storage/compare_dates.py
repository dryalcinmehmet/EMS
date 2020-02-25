import os
import sys
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import ExternalTaskSensor
from elasticsearch import Elasticsearch

es = Elasticsearch()
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float, Boolean, GeoPoint

sys.path.append(os.getcwd())


class BatteryModel(Document):
    ActivePower = Float()
    Temperature = Float()
    Humidity = Float()
    Weekdays = Integer()
    Vacays = Boolean()
    Location = GeoPoint()
    Date = Date()
    Place = Text(analyzer='standard', fields={'raw': Keyword()})

    class Index:
        name = 'default'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(BatteryModel, self).save(**kwargs)

    def SetValues(self, *args, **kwargs):
        self.ActivePower = args[0]
        self.Temperature = args[1]
        self.Humidity = args[2]
        self.Weekdays = args[3]
        self.Vacays = args[4]
        self.Location = args[5]
        self.Place = args[6]
        self.Date = args[7]

    def GetValues(self):
        print(self.ActivePower, self.Temperature, self.Humidity, self.Weekdays, self.Vacays, self.Location, self.Date,
              self.Place)


last_date_sql = context['task_instance'].xcom_pull(task_ids='select_mysql', key='last_date_sql')
last_date_es = context['task_instance'].xcom_pull(task_ids='get_es', key='last_date_es')
last_24 = context['task_instance'].xcom_pull(task_ids='select_mysql', key='last_24')
last_index_es = context['task_instance'].xcom_pull(task_ids='select_mysql', key='last_index_es')

def __start__(self, *args, **kwargs):
    BatteryObj = BatteryModel(meta={'id': kwargs['_id']})
    BatteryObj.SetValues(*args)
    BatteryModel.init(index=kwargs['index'])
    BatteryObj.save(**{'index': 'battery', 'id': 1})
    del BatteryObj

def compare(self):
    from collections import defaultdict
    args = defaultdict()
    if last_date_es < last_date_sql:

        for i in range(0, len(df['_id'])):
            for i in last_24.iloc[:, 3:].iloc[j]:
                args.append(i)
            __start__(args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                           **{'index': 'battery', '_id': args[7]})
    else:
        pass



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

host = "0.0.0.0"
dag = DAG('get_update_es',
               default_args=default_args,
               schedule_interval='@once',
               start_date=datetime(2017, 3, 20),
               catchup=False)



w_t = ExternalTaskSensor(task_id='wait_update_sql', external_dag_id='get_update_es',
                              external_task_id='get_es', dag=dag)

task1 = PythonOperator(task_id='compare_and_update',
                            provide_context=False,
                            python_callable=compare(),
                            dag=dag)

w_t >> task1

