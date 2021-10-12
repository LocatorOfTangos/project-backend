import requests
from src import config

# Make request
def auth_register_v2_request(email, password, name_first, name_last):
	return requests.post(config.url + 'auth/register/v2', json={
		'email': email,
		'password': password,
		'name_first': name_first,
		'name_last': name_last	
	})

def auth_login_v2_request(email, password):
	return requests.post(config.url + 'auth/login/v2', json={
		'email': email,
		'password': password,
	})

def clear_v1_request():
	return requests.delete(config.url + 'clear/v1', params={})

def channels_create_v2_request(token, name, is_public):
	return requests.post(config.url + 'channels/create/v2', json={
		'token': token,
		'name': name,
		'is_public': is_public
	})

def channel_join_v2_request(token, channel_id):
	return requests.post(config.url + 'channel/join/v2', json={
		'token': token,
		'channel_id': channel_id,
	})

def channel_details_v2_request(token, channel_id):
	return requests.get(config.url + 'channel/details/v2', params={
		'token': token,
		'channel_id': channel_id,
	})

def channel_invite_v2_request(token, channel_id, u_id):
	return requests.post(config.url + 'channel/invite/v2', json={
		'token': token,
		'channel_id': channel_id,
		'u_id': u_id
	})