import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

# USERS
@pytest.fixture
def user():
	return auth_register_v2_request('u1@mail.com', "psword", "first", "last").json()['token']

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
	return dm_create_v1_request(user, []).json()['dm_id']

@pytest.fixture
def d_msg(user, dm):
	return message_senddm_v1_request(user, dm, "Hello DM! Pin this, please.").json()['message_id']

# TESTS
def test_msg_pin_status(user, d_msg, c_msg):
    assert message_pin_v1_request(user, c_msg).status_code == 200
    assert message_pin_v1_request(user, d_msg).status_code == 200

def test_not_valid_msg_id(user2, d_msg, c_msg):
    assert message_pin_v1_request(user2, c_msg).status_code == 400
    assert message_pin_v1_request(user2, d_msg).status_code == 400

def test_not_owner(user, user2, channel, d_msg, c_msg):
    user2_id = auth_login_v2_request('u2@mail.com', 'psword').json()['auth_user_id']
    channel_invite_v2_request(user, channel, user2_id)
    message_pin_v1_request(user2, c_msg).status_code == 403

def test_pin_channel_msg(user, channel, c_msg):
    assert channel_messages_v2_request(user, channel, 0).json()['messages'][0]['is_pinned'] == False
    message_pin_v1_request(user, c_msg)
    assert channel_messages_v2_request(user, channel, 0).json()['messages'][0]['is_pinned'] == True
    message_unpin_v1_request(user, c_msg)
    assert channel_messages_v2_request(user, channel, 0).json()['messages'][0]['is_pinned'] == False

def test_pin_dm_msg(user, dm, d_msg):
    assert dm_messages_v1_request(user, dm, 0).json()['messages'][0]['is_pinned'] == False
    message_pin_v1_request(user, d_msg)
    assert dm_messages_v1_request(user, dm, 0).json()['messages'][0]['is_pinned'] == True
    message_unpin_v1_request(user, d_msg)
    assert dm_messages_v1_request(user, dm, 0).json()['messages'][0]['is_pinned'] == False