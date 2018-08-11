
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

def Controller(conf):
	if not 'type' in conf:
		raise ValueError('Missing controller type')
	if not 'host' in conf:
		raise ValueError('Missing controller host')
	
	type = conf['type']
	host = conf['host']
	
	username = conf.get('username', '')
	password = conf.get('password', '')
	
	if not host:
		raise ValueError('Invalid controller host')
	
	if type == 'ipcam':
		return IpCamController(host, username, password)
	else:
		raise ValueError('Invalid controller type')

class IpCamController:
	def __init__(self, host, username, password):
		self.host = host
		self.username = username
		self.password = password

	def command(self, action):
		print('Sending "{}" to camera at {}'.format(action, self.host))
		url = 'http://{}/cgi-bin/hi3510/'.format(self.host)
       
		if action == 'init':
			url+= 'param.cgi'
			params = { 'cmd': 'setmotorattr', '-tiltspeed': 1, '-panspeed': 1 }
		else:
			url+= 'ptzctrl.cgi'
			params = { '-step': 0, '-act': action, '-speed': 45 }
		
		auth = HTTPBasicAuth(self.username, self.password) if self.username or self.password else None
		try:
			req = requests.get(url, params=params, auth=auth)
			return req.ok
		except RequestException as e:
			print(e)
			return False

