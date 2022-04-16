from airflow.exceptions import AirflowException
from hooks.awx_hook import AWXHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

import logging
import pprint
import json

class AWXOperator(BaseOperator):
	"""
	Calls the AWX API for a given connection
	
	:param job_url: The url of the AWX job to be triggered
	:type job_url: string
	:param data: Data to customize the trigger of the AWX job
	:type data: dict
	"""
	
	ui_color = '#f4a578'
	
	@apply_defaults
	def __init__(self, job_url='', data={}, *args, **kwargs):
		
		super(AWXOperator, self).__init__(*args, **kwargs)
		
		self.job_url = job_url or 'https://awx.mhf.mhc/api/v2/job_templates/945/launch/'
		self.data = data or {"job_type": "check", "survey_enabled": "false", "extra_vars": {"msg": "my msg"}}
		
	def execute(self, context):
		logging.info("Initializing connection")
		awx = AWXHook()
		logging.info("Calling API")		
		response = awx.run(self.data, self.job_url)
