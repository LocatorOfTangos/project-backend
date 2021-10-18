import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

@pytest.fixture
def global_owner():
	return auth_register_v2_request('u4@mail.com', 'password', 'first', 'last')

@pytest.fixture
def ch_owner(global_owner):
	return auth_register_v2_request('u@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def user(global_owner):
	return auth_register_v2_request('u2@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def ch_pub(ch_owner):
	return channels_create_v2_request(ch_owner, "public", True).json()['channel_id']

@pytest.fixture
def msg(ch_pub, ch_owner):
	return message_send_v1_request(ch_owner, ch_pub, "message").json()['message_id']

### Helpers ###

# Get the text contents of message 'm_id' in channel 'c_id'
def contents(m_id, c_id):
	owner = global_owner()
	channel_join_v2_request(owner, c_id)
	messages = channel_messages_v2_request(owner, c_id, 0)['messages']
	for msg in messages:
		if msg['message_id'] == m_id:
			return msg['message']
	assert False

### Tests ###

def test_status_code(ch_owner, msg):
	assert message_edit_v1_request(ch_owner, msg, "new_message").status_code == 200

def test_return_type(ch_owner, msg):
	assert message_edit_v1_request(ch_owner, msg, "new_message").json() == {}

def test_successful_edit(ch_owner, msg):
	assert contents(msg, ch_pub) == 'message'
	message_edit_v1_request(ch_owner, msg, "new_message")
	assert contents(msg, ch_pub) == 'new_message'

def test_invalid_token(ch_owner, msg, ch_pub):
	# Not a token
	assert message_edit_v1_request(ch_owner, msg, "new_message").status_code == 200
	assert message_edit_v1_request("QWERTY", msg, "new_message").status_code == 403

	# Tampered token
	assert message_edit_v1_request(ch_owner[:-1] + '~', msg, "new_message").status_code == 403
	
	# Session ended
	assert message_edit_v1_request(ch_owner, msg, "new_message").status_code == 200
	auth_logout_v1_request(ch_owner)
	assert message_edit_v1_request(ch_owner, msg, "new_message").status_code == 403

def test_too_long(ch_owner, msg):
	assert message_edit_v1_request(ch_owner, msg, "a" * 1000).status_code == 200
	assert message_edit_v1_request(ch_owner, msg, "a" * 1001).status_code == 400

def test_invalid_msg_id(ch_owner):
	assert message_edit_v1_request(ch_owner, 12346578, "new_message").status_code == 400

def test_msg_in_different_channel(user, msg):
	# User attempts to edit a valid message, but in a channel they're not a member of
	assert message_edit_v1_request(user, msg, "new_message").status_code == 403

def test_global_owner_edit(global_owner, ch_pub, msg):
	assert contents(msg, ch_pub) == "message"
	channel_join_v2_request(global_owner, ch_pub)
	assert message_edit_v1_request(global_owner, msg, "new_message").status_code == 200
	assert contents(msg, ch_pub) == "new_message"

def test_ch_owner_edit(ch_owner, user, ch_pub):
	assert contents(msg, ch_pub) == "message"
	channel_join_v2_request(user, ch_pub)
	m_id = message_send_v1_request(user, ch_pub, "message").json()['message_id']
	assert message_edit_v1_request(ch_owner, m_id, "new_message").status_code == 200
	assert contents(msg, ch_pub) == "new_message"

def test_not_sender_edit(user, ch_pub, msg):
	assert contents(msg, ch_pub) == "message"
	channel_join_v2_request(user, ch_pub)
	assert message_edit_v1_request(user, msg, "new_message").status_code == 403
	assert contents(msg, ch_pub) == "message"

def test_delete(ch_owner, msg, ch_pub):
	assert message_edit_v1_request(ch_owner, msg, "").status_code == 200
	# Ensure that no message matching the ID exists
	assert not any(m['message_id'] == msg for m in channel_messages_v2_request(ch_owner, ch_pub, 0)['messages'])