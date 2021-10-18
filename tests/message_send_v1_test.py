import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

@pytest.fixture
def ch_owner():
	return auth_register_v2_request('u@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def user():
	# Register an unused user to ensure not global owner
	auth_register_v2_request('u1@mail.com', 'password', 'first', 'last')
	return auth_register_v2_request('u2@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def ch_pub(ch_owner):
	return channels_create_v2_request(ch_owner, "public", True).json()['channel_id']

@pytest.fixture
def ch_priv(ch_owner):
	return channels_create_v2_request(ch_owner, "private", False).json()['channel_id']


#### Tests ####

def test_status_code(ch_owner, ch_pub):
	assert message_send_v1_request(ch_owner, ch_pub, "message").status_code == 200

def test_return_type(ch_owner, ch_pub):
	resp = message_send_v1_request(ch_owner, ch_pub, "message").json()
	assert resp.keys() == ['message_id']
	assert isinstance(resp['message_id'], int)

def test_message_ids_unique_single_channel(ch_owner, ch_pub):
	used_ids = set()
	assert message_send_v1_request(ch_owner, ch_pub, "m").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "n").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "o").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "p").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "q").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "r").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "s").json()['messsage_id'] not in used_ids

def test_message_ids_unique_multiple_channels(ch_owner, ch_pub, ch_priv):
	used_ids = set()
	assert message_send_v1_request(ch_owner, ch_pub, "m").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_priv, "n").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "o").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_priv, "p").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "q").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_priv, "r").json()['messsage_id'] not in used_ids
	assert message_send_v1_request(ch_owner, ch_pub, "s").json()['messsage_id'] not in used_ids

def test_invalid_ch_id(ch_owner):
	assert message_send_v1_request(ch_owner, 12346578, "message").status_code == 400

def test_invalid_token(user, ch_pub):
	# Not a token
	assert message_send_v1_request("QWERTY", ch_pub, "message").status_code == 403

	# Tampered token
	assert message_send_v1_request(user[:-1] + '~', ch_pub, "message").status_code == 403
	
	# Session ended
	assert message_send_v1_request(user, ch_pub, "message").status_code == 200
	auth_logout_v1_request(user)
	assert message_send_v1_request(user, ch_pub, "message").status_code == 403

def test_invalid_msg_len(ch_owner, ch_pub):
	# Too short
	assert message_send_v1_request(ch_owner, ch_pub, "").status_code == 400
	
	# OK
	assert message_send_v1_request(ch_owner, ch_pub, "a").status_code == 200
	assert message_send_v1_request(ch_owner, ch_pub, "a" * 1000).status_code == 200
	
	# Too long
	assert message_send_v1_request(ch_owner, ch_pub, "a" * 1001).status_code == 400

def test_not_member_public(user, ch_pub):
	assert message_send_v1_request(user, ch_pub, "message").status_code == 403

def test_not_member_private(user, ch_priv):
	assert message_send_v1_request(user, ch_priv, "message").status_code == 403

@pytest.mark.skip(reason='Requires channel/leave')
def test_left_channel(ch_owner, ch_pub):
	assert message_send_v1_request(ch_owner, ch_pub, "message").status_code == 200
	channel_leave_v1_request(ch_owner, ch_pub)
	assert message_send_v1_request(ch_owner, ch_pub, "message").status_code == 403
