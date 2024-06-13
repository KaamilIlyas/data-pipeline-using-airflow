import requests
from bs4 import BeautifulSoup
import pendulum
import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.models import Variable

sources = ['https://www.dawn.com/', 'https://www.bbc.com/']

def extract():
    links = [[] for _ in sources]
    df_links = pd.DataFrame(columns=['link', 'title', 'description'])

    for i, source in enumerate(sources):
        try:
            data = requests.get(source)
            html_data = BeautifulSoup(data.text, 'html.parser')
            links[i] = [j['href'] for j in html_data.find_all('a', href=True)]
        except Exception as e:
            print(f"Error fetching {source}: {e}")
            continue

    for source_links in links:
        for idx, link in enumerate(source_links):
            if idx == 30:
                break

            try:
                j_data = requests.get(link)
                if j_data.status_code != 200:
                    continue

                j_soup = BeautifulSoup(j_data.text, 'html.parser')

                title = j_soup.find('title')
                if title:
                    title = title.get_text()
                else:
                    continue

                description = " ".join([p.get_text() for p in j_soup.find_all('p')])
                if not description:
                    continue

                df_links = pd.concat([df_links, pd.DataFrame({'link': [link], 'title': [title], 'description': [description]})], ignore_index=True)
            except Exception as e:
                print(f"Error processing {link}: {e}")
                continue

    Variable.set("df_links", df_links.to_json(), serialize_json=True)

def transform(**kwargs):
    print("Transformation")

def load(**kwargs):
    # df_links_json = Variable.get("df_links", deserialize_json=True)
    # df_links = pd.read_json(df_links_json)

    # df_links.to_csv('/opt/airflow/dags/data/link_data.csv', index=False)

    # dvc_command = ['cd "C:/Users/This/Desktop/Airflow_/dags"', 'dvc add ./data/link_data.csv', 'dvc push']
    # git_command = ['cd "C:/Users/This/Desktop/Airflow_/dags"', 'git add .', 'git commit -m "New Dataset"', 'git push origin master'] 

    # os.system(' && '.join(dvc_command))
    # os.system(' && '.join(git_command))
    print("Kamil Ilyas")

default_args = {
    'owner': 'Kamil'
}

@dag(
    dag_id='mlops-a2-dag',
    default_args=default_args,
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    description='A simple demo of airflow'
)
def tasks():
    task1 = PythonOperator(
        task_id="Task_1",
        python_callable=extract
    )

    task2 = PythonOperator(
        task_id="Task_2",
        python_callable=transform
    )

    task3 = PythonOperator(
        task_id="Task_3",
        python_callable=load
    )

    task1 >> task2 >> task3

dag = tasks()