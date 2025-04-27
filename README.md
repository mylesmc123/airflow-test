# Steps to setup airflow server


🎯 Quick Recap:
conda create -n airflow python=3.10

#### Temp variable
export AIRFLOW_HOME=~/airflow

pip install apache-airflow with constraints

airflow db init

airflow users create \
  --username admin \
  --firstname First \
  --lastname Admin \
  --role Admin \
  --email admin@example.com \
  --password admin

Start the webserver + scheduler
### Terminal 1: Start the webserver
airflow webserver --port 8080

#### Terminal 2: Start the scheduler
airflow scheduler

# Get RFC Data
get_gage_data.py

# Setup Airflow Trigger based on gage threshold
