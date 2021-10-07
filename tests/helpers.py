import requests
import json
from src import config

# Return true if two responses have the same text component
def response_comp(a, b):
	return json.loads(a.text) == json.loads(b.text)

# Make request
def auth_register_v2_request(email, password, name_first, name_last):
	return requests.post(config.url + 'auth/register/v2', params={
		'email': email,
		'password': password,
		'name_first': name_first,
		'name_last': name_last	
	})

def auth_login_v2_request(email, password):
	return requests.post(config.url + 'auth/login/v2', params={
		'email': email,
		'password': password,
	})