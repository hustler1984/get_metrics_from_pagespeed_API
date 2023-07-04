from airflow import DAG
from airflow.operators.python import PythonOperator

import datetime as dt
import os
import numpy as np
from clickhouse_driver import Client
import pandas as pd
import requests

#Добавляем переменную окружения
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")

DAG_ID = "LOAD_SITE_METRICS_v1"
default_args = {
    'owner': 'goryachev_v',
    'email': "goryachev_v@xxx.ru",
    'email_on_failure': True,
    'depends_on_past': False,
    'retries': 5,
    'retry_delay': dt.timedelta(minutes = 5)
}
#
# добавляем ключ АПИ
api_key = 'PUT_YOUR_API_KEY'

def extract_data():
    #считываем список URL из файла в репозитории гит хаба.
    data = pd.read_csv('https://raw.githubusercontent.com/grimlyrosen/tests/main/urllist.csv')
    url_list = list(data.url.values)

    # создаём пустой список для хранения данных
    lst = []

    # итерируемся по списку URL
    for url in url_list:
        # сюда по хорошему надо добавить блок try except, чтобы ловить ошибки
        # https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
        response = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+url+'&strategy='+mode+'&key='+api_key)
        js = response.json()
        TBT = js['lighthouseResult']['audits']['total-blocking-time']['numericValue']
        LCP = js['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']
        dti = pd.to_datetime(dt.datetime.strptime(js['analysisUTCTimestamp'][:-5], '%Y-%m-%dT%H:%M:%S'))
        lst.append([dti,url,'TBT',TBT])
        lst.append([dti,url,'LCP',LCP])
    DataToLoad = pd.DataFrame(lst, columns=["DDATE","URL","METRICS","VALUE"])
    # возвращаем данные для загрузки в виде Pandas DataFrame
    return DataToLoad

def load_data():
    client = Client(host='YOUR_HOST',
                    user='YOUR_USERNAME',
                    password='YOUR_PASSWORD')
    DATA_TO_LOAD = extract_data()
    # Вставляем данные
    client.insert_dataframe('INSERT INTO test.site_metrics VALUES', DATA_TO_LOAD, settings={"use_numpy":True,"insert_block_size":DATA_TO_LOAD.shape[0]})

with DAG(dag_id = DAG_ID,
        start_date=dt.datetime(2023, 7, 4),
        schedule_interval='00 08 * * *',
        catchup = False,
        tags=['table_creation'],
        default_args=default_args) as dag:
    load_data = PythonOperator(
        task_id='load_to_ch',
        python_callable=load_data,
        retries=1)

    load_data