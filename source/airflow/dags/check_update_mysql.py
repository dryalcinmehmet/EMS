from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float, Boolean,GeoPoint,connections
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from pandasticsearch import Select
from espandas import Espandas
from airflow import DAG
import sqlalchemy as sql
import psycopg2
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
          schedule_interval='@hourly',
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
            es = Elasticsearch('172.21.0.4')
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
            BatteryObj.save(**{'index': 'battery_test', 'id': 1})
            del BatteryObj

    def get_mysql():
        import mysql.connector

        mydb = mysql.connector.connect(
            host="10.212.92.60",
            user="arge_trafo",
            passwd="Ar!gTR19",
            database="osos")

        mycursor = mydb.cursor()

        q = "select * from arge_trafo_load_profile"
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        df_sql = pd.DataFrame(myresult, columns=['Date_Time', 'Trafo_id', 'Active_Energy'])


        q = "select * from arge_trafo_load_profile order by Date_Time asc limit 24"
        mycursor.execute(q)
        myresult_24 = mycursor.fetchall()
        df_sql_24 = pd.DataFrame(myresult_24, columns=['Date_Time', 'Trafo_id', 'Active_Energy'])

        q = "select Date_Time from arge_trafo_load_profile order by Date_Time desc limit 1"
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        last_date = pd.DataFrame(myresult, columns=['Date_Time'])['Date_Time'][0]

        return df_sql,df_sql_24,last_date

    def first_select(df_sql):
        connection = psycopg2.connect(user="airflow",
                                      password="airflow",
                                      host="postgres",
                                      port="5432",
                                      database="airflow")
        cursor = connection.cursor()

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS arge_trafo_load_profile ( Trafo_id VARCHAR(30) NOT NULL,Date_Time TIMESTAMP NOT NULL, Active_Energy float);''')
        connection.commit()
        for idx, i in df_sql.iterrows():
            cursor.execute("INSERT INTO arge_trafo_load_profile VALUES (%s, %s, %s);",
                           (i[0], i[1], i[2]))
        connection.commit()

        connections.create_connection(hosts=['172.21.0.4'])
        import uuid
        from elasticsearch import Elasticsearch
        from elasticsearch import helpers

        cols=['Trafo_id', 'Date_Time', 'Active_Energy', 'Temperature', 'Humidity']

        class BatteryModel(Document):
            Trafo_id = Float()
            Date_Time = Date()
            Active_Energy = Float()
            Temperature = Integer()
            Humidity = Integer()

            class Index:
                name = 'default'
                settings = {
                    "number_of_shards": 2,
                }

            def save(self, **kwargs):
                return super(BatteryModel, self).save(**kwargs)

            def SetValues(self, *args, **kwargs):
                print(**kwargs)
                self.Trafo_id = args[0]
                self.Date_Time = args[1]
                self.Active_Energy = args[2]
                self.Temperature = args[3]
                self.Humidity = args[4]

            def get(self, *args, **kwargs):
                documents = es.search(index="{}".format(args[0]),
                                      body={"query": {"match_all": {}}, "sort": {"_id": "desc"}, "size": args[1]})
                df = Select.from_dict(documents).to_pandas()
                return df

        class Main:
            def __init__(self):
                print("Starting Process..")

            def __start__(self, *args, **kwargs):
                print(kwargs['_id'])
                BatteryObj = BatteryModel(meta={'id': kwargs['_id']})
                BatteryObj.SetValues(*args)
                BatteryModel.init(index=kwargs['index'])
                BatteryObj.save(**{'index': 'battery_test', 'id': kwargs['_id']})
                del BatteryObj

        # df = Query().get('test0',10000)
        # q = BatteryModel.get(_id=1)
        m = Main()
        es=Elasticsearch(hosts=['172.21.0.4'])
        for index, document in df_sql.iterrows():
            m.__start__(document[0],
                        document[1],
                        document[2],
                        document[3],
                        document[4],
                        **{'index': 'battery_test', '_id': uuid.uuid1()})


    def get_es():
        try:
            connections.create_connection(hosts=['172.21.0.4'])
            df_es = Query().get('arge_trafo_load_profile', 10000)
            df_es = df_es.sort_values('Date_Time', ascending=True)
            last_date_es = [i for i in df_es[-1::]['Date_Time']][0]
            last_index_es = [i for i in df_es[-1::]['_id']][0]
            try:
                last_index_es+1
            except:
                last_index_es=1
        except:
            last_index_es=1
            last_date_es = ''
        return last_date_es,last_index_es

    def weather_and_weekday(df):


        df['Temperature'] =  [i for i in range(0,len(df))]
        df['Humidity'] =   [i for i in range(0,len(df))]

        return df

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
            '''CREATE TABLE IF NOT EXISTS arge_trafo_load_profile ( Trafo_id VARCHAR(30) NOT NULL,Date_Time TIMESTAMP NOT NULL, Active_Energy float);''')
        connection.commit()


        cursor.execute("SELECT * FROM arge_trafo_load_profile ORDER BY Date_Time DESC LIMIT 24;")


        result = cursor.fetchall()
        import pandas as pd
        df_sql_24 = pd.DataFrame(result, columns=['Trafo_id', 'Date_Time', 'Active_Energy'])
        try:
            last_date_postgres = d['Date_Time'][0]
        except:
            last_date_postgres= datetime(2000, 11, 28, 23, 55, 59)
            cursor.close()
            connection.close()
            "No data!"
        return last_date_postgres,df_sql_24

    def del_postgress():


        connection = psycopg2.connect(user="airflow",
                                      password="airflow",
                                      host="postgres",
                                      port="5432",
                                      database="airflow")
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''drop table arge_trafo_load_profile; ''')
            connection.commit()
            cursor.close()
        except:
            pass
        connection.close()

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
                cursor.execute("INSERT INTO arge_trafo_load_profile VALUES (%s, %s, %s);",(i[0], i[1], i[2]))
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

        connections.create_connection(hosts=['172.21.0.4'])
        import uuid
        from elasticsearch import Elasticsearch
        from elasticsearch import helpers

        cols=['Trafo_id', 'Date_Time', 'Active_Energy', 'Temperature', 'Humidity']

        class BatteryModel(Document):
            Trafo_id = Float()
            Date_Time = Date()
            Active_Energy = Float()
            Temperature = Integer()
            Humidity = Integer()

            class Index:
                name = 'default'
                settings = {
                    "number_of_shards": 2,
                }

            def save(self, **kwargs):
                return super(BatteryModel, self).save(**kwargs)

            def SetValues(self, *args, **kwargs):
                print(**kwargs)
                self.Trafo_id = args[0]
                self.Date_Time = args[1]
                self.Active_Energy = args[2]
                self.Temperature = args[3]
                self.Humidity = args[4]

            def get(self, *args, **kwargs):
                documents = es.search(index="{}".format(args[0]),
                                      body={"query": {"match_all": {}}, "sort": {"_id": "desc"}, "size": args[1]})
                df = Select.from_dict(documents).to_pandas()
                return df

        class Main:
            def __init__(self):
                print("Starting Process..")

            def __start__(self, *args, **kwargs):
                print(kwargs['_id'])
                BatteryObj = BatteryModel(meta={'id': kwargs['_id']})
                BatteryObj.SetValues(*args)
                BatteryModel.init(index=kwargs['index'])
                BatteryObj.save(**{'index': 'battery_test', 'id': kwargs['_id']})
                del BatteryObj
        m = Main()
        for index, document in df_sql_24.iterrows():
            m.__start__(document[0],
                        document[1],
                        document[2],
                        document[3],
                        document[4],
                        **{'index': 'battery_test', '_id': uuid.uuid1()})

    def check_last_update(last_date_sql,last_date_postgres,df_sql_24):

        if last_date_sql > last_date_postgres:
            insert2postgres(df_sql_24)
            df_sql_24 = weather_and_weekday(df_sql_24)
            insert_es(df_sql_24)

    def ml():
        from math import sqrt
        from numpy import concatenate
        from pandas import DataFrame
        from datetime import datetime
        from pandas import concat
        import pandas as pd
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import LabelEncoder
        from sklearn.metrics import mean_squared_error
        from keras.models import Sequential
        from keras.layers import Dense
        from keras.layers import LSTM
        import random



        def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
            n_vars = 1 if type(data) is list else data.shape[1]
            df = DataFrame(data)
            cols, names = list(), list()
            # input sequence (t-n, ... t-1)
            for i in range(n_in, 0, -1):
                cols.append(df.shift(i))
                names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
            # forecast sequence (t, t+1, ... t+n)
            for i in range(0, n_out):
                cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
                # put it all together
            agg = concat(cols, axis=1)
            agg.columns = names
            # drop rows with NaN values
            if dropnan:
                agg.dropna(inplace=True)
            return agg


        from pandasticsearch import Select
        from elasticsearch import Elasticsearch
        import elasticsearch.helpers
        es = Elasticsearch(['172.21.0.4'])
        body = {"query": {"match_all": {}}}
        results = elasticsearch.helpers.scan(es, query=body, index="battery_test")
        df = pd.DataFrame.from_dict([document['_source'] for document in results])

        dataset = df.drop(columns=['Trafo_id'])
        dataset = dataset.set_index('Date_Time')
        values = dataset.values
        encoder = LabelEncoder()
        values[:, 1] = encoder.fit_transform(values[:, 1])
        values = values.astype('float32')
        # normalize features
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(values)
        # specify the number of lag hours
        n_hours = 5
        n_features = 3
        # frame as supervised learning
        reframed = series_to_supervised(scaled, n_hours, 1)
        print(reframed.shape)

        # split into train and test sets
        values = reframed.values
        n_train_hours = (len(dataset)-24) * 24
        train = values[:n_train_hours, :]
        test = values[n_train_hours - 5:, :]
        # split into input and outputs
        n_obs = n_hours * n_features
        train_X, train_y = train[:, :n_obs], train[:, -n_features]
        test_X, test_y = test[:, :n_obs], test[:, -n_features]
        print(train_X.shape, len(train_X), train_y.shape)
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
        test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
        print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
        # design network
        model = Sequential()
        model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        # fit network
        history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2,
                            shuffle=False)

        # make a prediction
        yhat = model.predict(test_X)
        test_X = test_X.reshape((test_X.shape[0], n_hours * n_features))
        # invert scaling for forecast
        inv_yhat = concatenate((yhat, test_X[:, -3:]), axis=1)
        inv_yhat = scaler.inverse_transform(inv_yhat)
        inv_yhat = inv_yhat[:, 0]
        # invert scaling for actual
        test_y = test_y.reshape((len(test_y), 1))
        inv_y = concatenate((test_y, test_X[:, -3:]), axis=1)
        inv_y = scaler.inverse_transform(inv_y)
        inv_y = inv_y[:, 0]
        # calculate RMSE
        rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
        print('Test RMSE: %.3f' % rmse)
        model.summary()
        from sklearn.metrics import r2_score
        score = r2_score(inv_y, inv_yhat)
        print('Train Score is:', score)

        invyhat = pd.DataFrame(data=inv_yhat)


        class pred(Document):
            invyhat = Float()

            class Index:
                name = 'default'
                settings = {
                    "number_of_shards": 2,
                }

            def save(self, **kwargs):
                return super(pred, self).save(**kwargs)

            def SetValues(self, *args, **kwargs):
                print(**kwargs)
                self.invyhat = args[0]



        class Main:
            def __init__(self):
                print("Starting Process..")

            def __start__(self, *args, **kwargs):
                print(kwargs['_id'])
                BatteryObj = pred(meta={'id': kwargs['_id']})
                BatteryObj.SetValues(*args)
                pred.init(index=kwargs['index'])
                BatteryObj.save(**{'index': 'pred_test', 'id': kwargs['_id']})
                del BatteryObj
        m = Main()
        for index, document in invyhat.iterrows():
            m.__start__(document[0],
                        **{'index': 'pred_test', '_id': uuid.uuid1()})


    # del_postgress()
    # df, df_sql_24, last_date_sql=get_mysql()
    # # df = weather_and_weekday(df)
    # # first_select(df)
    #
    # # last_date_es, last_index_es = get_es()
    # last_date_postgres, df_sql_24 = get_postgres()
    # #
    # check_last_update(last_date_sql,last_date_postgres,df_sql_24)
    ml()



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


