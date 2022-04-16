from builtins import str
import logging
import pprint
import json
import requests

from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException


class AWXHook(BaseHook):
	"""
	Interact with AWX API
	"""

	def __init__(self):
		self.authToken = None
		self.authUrl = 'https://awx.mhf.mhc/api/v2/tokens/'
	
	def getAuthedConnection(self):
		"""
		Obtains an authenticated connection
		"""
		session = requests.Session()

		session.headers.update({'Content-Type': 'application/json','Authorization': 'Basic YWlyZmxvdzpBd2FlTmVvNXNhaWtvVjR3cGhlaTVJYTZlYWtpNkRlMA=='})
		
		if not self.authToken:
			self.getAuthToken(session, "", "")
		
		session.headers.update({ 'X-Auth-Token': self.authToken })
		return session;
	
	def getAuthToken( self, session, username, password ):
		"""
		Gets auth token from the AWX API
		"""
		self.authToken = None
		url = self.authUrl
		
		request = requests.Request('POST', url)
		prepped_request = session.prepare_request(request)
		
		response = session.send(prepped_request, stream=False, verify=False, allow_redirects=True)
		resp = response.json()

		if resp.get('token'):
			self.authToken = resp['token']
		else:
			raise AirflowException( 'Could not authenticate properly: ' + str(response.status_code) + ' ' + response.reason )
		
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError:
			raise AirflowException( 'Could not authenticate properly: ' + str(response.status_code) + ' ' + response.reason )
		return self.authToken
	
	def run( self, custom_data={}, job_url='' ):
		"""
		Calls the AWX API
		"""
		session = self.getAuthedConnection()
		url = job_url
		data = custom_data
		
		try:
			request = requests.Request('POST', url)
			prepped_request = session.prepare_request(request)
			prepped_request.body = json.dumps(data)
			prepped_request.headers.update({ 'Content-Length': len(prepped_request.body) });
			
			response = session.send(prepped_request, stream=False, verify=False, allow_redirects=True)
			response.raise_for_status()
		except requests.exceptions.HTTPError:
			logging.error( 'HTTP error: ' + response.reason )
		
		logging.info( 'DEBUG: ' + pprint.pformat( response.__dict__ ) )
		
		return response



