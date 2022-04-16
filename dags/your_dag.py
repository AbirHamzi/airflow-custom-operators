from airflow import DAG
from datetime import datetime, timedelta
from operators.awx_operator import AWXOperator

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2018, 1, 1),
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}


with DAG('customdag',
		 max_active_runs=3,
		 schedule_interval='@once',
		 default_args=default_args) as dag:


	awx_test = AWXOperator(task_id='awx-task', job_url='https://awx.mhf.mhc/api/v2/job_templates/945/launch/',data={"job_type": "check", "survey_enabled": "false", "extra_vars": {"msg": "my msg"}})



	awx_test