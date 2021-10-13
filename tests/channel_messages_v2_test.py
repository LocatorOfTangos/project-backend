import pytest

from src.make_request import *

@pytest.fixture
def clear():
	clear_v1_request()

@pytest.fixture
def user():
	u_id = auth_register_v2_request("user@mail.com", "password", "first", "last").json()['token']
	return u_id

@pytest.fixture
def channel(user):
	c_id = channels_create_v2_request(user, "channel", True)['channel_id'] # User automatically added to channel
	return c_id

# Tests:

def test_invalid_channel_id(clear, user, channel):
	assert channel_messages_v2_request(user, -1, 0).status_code == 400
	assert channel_messages_v2_request(user, 5, 0).status_code == 400

def test_valid_no_messages(clear, user, channel):
	assert channel_messages_v2_request(user, channel, 0).json() == {'messages': [], 'start':0, 'end':-1}

def test_messages_list_len(clear, user, channel):
	assert 0 <= len(channel_messages_v2_request(user, channel, 0).json()['messages']) <= 50

def test_invalid_user(clear, channel):
	assert channel_messages_v2_request(12365478, channel, 0).status_code == 403

def test_invalid_start(clear, user, channel):
	assert channel_messages_v2_request(user, channel, 5).status_code == 400
	assert channel_messages_v2_request(user, channel, -5).status_code == 400

def test_not_member(clear, channel):
	user_unauthorised = auth_register_v2_request("user2@mail.com", "password", "first", "last").json()['auth_user_id']
	assert channel_messages_v2_request(user_unauthorised, channel, 0).status_code == 403

@pytest.mark.skip(reason="Send message not implemented yet")
def messages_test():
	pass