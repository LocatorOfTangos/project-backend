import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

# USERS
@pytest.fixture
def user():
	return auth_register_v2_request('e@mail.com', "psword", "first", "last").json()['token']

@pytest.fixture
def user2():
	return auth_register_v2_request('u2@mail.com', "psword", "first", "last").json()['token']

# CHANNEL
@pytest.fixture
def channel(user):
	return channels_create_v2_request(user, "channel", True).json()['channel_id']

@pytest.fixture
def c_msg(user, channel):
	return message_send_v1_request(user, channel, "Hello channel! Pin this, please.").json()['message_id']

# DM
@pytest.fixture
def dm(user, user2):
	return dm_create_v1_request(user, [])['dm_id']

@pytest.fixture
def d_msg(user, dm):
	return message_senddm_v1_request(user, dm, "Hello DM! Pin this, please.").json()['message_id']

# TESTS
def channel_msg_pin_test(user, c_msg):
    assert message_pin_v1_request(user, c_msg).status_code == 200
    assert message_pin_v1_request(user, d_msg).status_code == 200

def not_valid_msg_id():
    assert message_pin_v1_request(user2, c_msg).status_code == 400
    assert message_pin_v1_request(user2, d_msg).status_code == 400