from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float, Boolean,GeoPoint,connections
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from pandasticsearch import Select
from airflow import DAG
import sqlalchemy as sql
import pandas as pd
import random
import sys
import os

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

dag = DAG('check_update_mysql',
          default_args=default_args,
          schedule_interval='@once',
          start_date=datetime(2017, 3, 20),
          catchup=False)


def process(**kwargs):
    class BatteryModel(Document):
        Trafo_id = Text()
        Date_Time = Date()
        Active_Energy = Float()
        Temperature = Float()
        Weekday = Integer()
        Location = GeoPoint()
        Place = Text(analyzer='standard', fields={'raw': Keyword()})

        class Index:
            name = 'default'
            settings = {
                "number_of_shards": 2,
            }

        def save(self, **kwargs):
            return super(BatteryModel, self).save(**kwargs)

        def SetValues(self, *args, **kwargs):
            self.Trafo_id = args[0]
            self.Date_Time = args[1]
            self.Active_Energy = args[2]
            self.Temperature = args[3]
            self.Weekday = args[4]
            self.Location = args[5]
            self.Place = args[6]

    class Query:
        def __init___(self, *args, **kwargs):
            self.IndexName = args[0]
            self.Size = args[1]

        def get(self, *args, **kwargs):
            es = Elasticsearch()
            documents = es.search(index="{}".format(args[0]),
                                  body={"query": {"match_all": {}}, "sort": {"_id": "desc"}, "size": args[1]})
            df = Select.from_dict(documents).to_pandas()
            return df

    class Main:
        def __init__(self):
            print("Starting Process..")

        def __start__(self, *args, **kwargs):
            BatteryObj = BatteryModel(meta={'id': kwargs['_id']})
            BatteryObj.SetValues(*args)
            BatteryModel.init(index=kwargs['index'])
            BatteryObj.save(**{'index': 'battery', 'id': 1})
            del BatteryObj

    def get_mysql():
        import mysql.connector

        mydb = mysql.connector.connect(
            host="176.234.4.185",
            user="root",
            passwd="root",
            database="test")

        mycursor = mydb.cursor()

        q = "select * from test"
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        df_sql = pd.DataFrame(myresult, columns=['Date_Time', 'Trafo_id', 'Active_Energy'])

        q = "select * from test order by Date_Time asc limit 12"
        mycursor.execute(q)
        myresult_24 = mycursor.fetchall()
        df_sql_24 = pd.DataFrame(myresult_24, columns=['Date_Time', 'Trafo_id', 'Active_Energy'])

        q = "select Date_Time from test order by Date_Time desc limit 1"
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        last_date = pd.DataFrame(myresult, columns=['Date_Time'])['Date_Time'][0]
        return df_sql,df_sql_24,last_date



    def get_es():
        try:
            connections.create_connection(hosts=['172.18.0.3'])
            df_es = Query().get('arge_trafo_load_profile', 10000)
            df_es = df_es.sort_values('Date_Time', ascending=True)
            last_date_es = [i for i in df_es[-1::]['Date_Time']][0]
            last_index_es = [i for i in df_es[-1::]['_id']][0]
        except:
            last_index_es=-1
            last_date_es = ''
        return last_date_es,last_index_es

    def weather_and_weekday(df_sql_24):

        def calculate_day(d):
            day = pd.to_datetime(d, errors='coerce')
            return day.dt.dayofweek
        from selenium import webdriver
        import time
        import requests
        from bs4 import BeautifulSoup

        driver = webdriver.Chrome(executable_path='chromedriver')
        page = driver.get( "https://weather.com/en-IN/weather/hourbyhour/l/b37d8353bec8f45cd4dc9d9ca20ea925235f0765073b23015dd213d8d8d49057")

        for i in range(3):
            time.sleep(2)
            driver.find_element_by_xpath("//button[@class='styles__btnLink__2mxiC styles__displayBtn__YPvCm']").click()

        # page = requests.get("https://weather.com/en-IN/weather/hourbyhour/l/b37d8353bec8f45cd4dc9d9ca20ea925235f0765073b23015dd213d8d8d49057")
        time.sleep(1)

        page_source = driver.page_source

        time.sleep(1)

        soup = BeautifulSoup(page_source, "html.parser")

        all = soup.find("div", {"class": "locations-title hourly-page-title"}).find("h1").text
        table = soup.find_all("table", {"class": "twc-table"})
        l = []
        for items in table:
            for i in range(len(items.find_all("tr")) - 1):
                d = {}
                #  d["day"]=items.find_all("span",{"class":"date-time"})[i].text
                d["date"] = items.find_all("span", {"class": "dsx-date"})[i].text
                d["temp"] = items.find_all("td", {"class": "temp"})[i].text

                l.append(d)



        df_sql_24['temp'] =  pd.DataFrame(l)['temp'][0:24]
        df_sql_24['weekday'] =  calculate_day(df_sql_24['Date_Time'])

        return df_sql_24

    def get_postgres():
        last_date_postgres=''

        import psycopg2
        connection = psycopg2.connect(user="airflow",
                                      password="airflow",
                                      host="postgres",
                                      port="5432",
                                      database="airflow")
        cursor = connection.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS arge_trafo_load_profile ( Trafo_id VARCHAR(30) NOT NULL,Date_Time TIMESTAMP NOT NULL, Active_Energy float,Temperature float,Weekday float);''')
        connection.commit()


        cursor.execute("SELECT * FROM arge_trafo_load_profile ORDER BY Date_Time DESC LIMIT 1;")
        result = cursor.fetchall()
        import pandas as pd
        d = pd.DataFrame(result, columns=['Trafo_id', 'Date_Time', 'Active_Power','Temperature','Weekday'])
        try:
            last_date_postgres = d['Date_Time'][0]
        except:
            last_date_postgres= datetime(2000, 11, 28, 23, 55, 59)
            cursor.close()
            connection.close()
            "No data!"
        return last_date_postgres

    def insert2postgres(df_sql_24):
        import psycopg2
        #postgres
        try:
            connection = psycopg2.connect(user="airflow",
                                          password="airflow",
                                          host="postgres",
                                          port="5432",
                                          database="airflow")
            cursor = connection.cursor()
            for idx, i in df_sql_24.iterrows():
                cursor.execute("INSERT INTO arge_trafo_load_profile VALUES (%s, %s, %s, %s, %s);",(i[0], i[1], i[2], i[3], i[4]))
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def insert_es(df_sql_24):
        connections.create_connection(hosts=['172.18.0.3'])
        m = Main()
        for j in range(len(df_sql_24['Date_Time'])):
            for i in df_sql_24.loc[j]:
                m.__start__(i[0], i[1], i[2], i[3], i[4], "41.055137,28.979530", "Taskim", **{'index': 'arge_trafo_load_profile', '_id': last_index_es + 1})

    def check_last_update(last_date_sql,last_date_postgres,df_sql_24):

        if last_date_sql > last_date_postgres:
            insert2postgres(df_sql_24)
            # insert_es(df_sql_24)



    df, df_sql_24, last_date_sql=get_mysql()
    # last_date_es, last_index_es = get_es()
    df_sql_24 = weather_and_weekday(df_sql_24)
    last_date_postgres=get_postgres()
    check_last_update(last_date_sql,last_date_postgres,df_sql_24)



def pull_function(**kwargs):
    task_instance = kwargs['task_instance']
    mysql_vars = task_instance.xcom_pull(task_ids='connect_mysql',key='mysql_vars')
    import json
    with open('mysql_vars.json', 'w') as f:
        json.dump(mysql_vars, f)



sql = PythonOperator(task_id='connect_mysql',
                       provide_context=True,
                       python_callable=process,
                       dag=dag)



pull_task = PythonOperator(
                task_id='pull_task',
                python_callable=pull_function,
                provide_context=True,
                dag=dag)






#Here we go!
sql >> pull_task


