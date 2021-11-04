import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

# USERS
@pytest.fixture
def user():
	return auth_register_v2_request('e@mail.com', "psword", "first", "last").json()['token']

# CHANNEL
@pytest.fixture
def channel(user):
	return channels_create_v2_request(user, "channel", True).json()['channel_id']

@pytest.fixture
def c_msg(user, channel):
	return message_send_v1_request(user, channel, "Hello world").json()['message_id']

# DM
@pytest.fixture
def dm(user, user2):
	return dm_create_v1_request(user, [])['dm_id']

@pytest.fixture
def d_msg(user, dm):
	return message_senddm_v1_request(user, dm, "Hello world").json()['message_id']

# TESTS
def channel_msg_pin_test(user, c_msg):
    assert message_pin_v1_request(user, c_msg).status_code == 200
