import requests
from src import config

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

def clear_v1_request():
	return requests.delete(config.url + 'clear/v1', params={})