import pytest
from src.make_request_test import *

@pytest.fixture
def sender():
	return auth_register_v2_request("e@mail.com", "psword", "first", "last").json()['token']

@pytest.fixture
def channel1(sender):
	return channels_create_v2_request(sender, "channel1", True).json()['channel_id']

@pytest.fixture
def channel2(sender):
	return channels_create_v2_request(sender, "channel2", True).json()['channel_id']

@pytest.fixture
def user(channel):
	user = auth_register_v2_request("u@mail.com", "psword", "first", "last").json()['token']
	channel_join_v2_request(user, channel)
	return user

@pytest.fixture
def dm(user):
	return dm_create_v1_request(user, []).json()['dm_id']

@pytest.fixture
def message(user, channel1):
	return message_send_v1_request(user, channel1, "The world is flat").json()['message_id']


def test_status(user, message, channel2):
	assert message_share_v1_request(user, message, "This guy agrees", channel2, -1).status_code == 200

def test_channel_and_dm_invalid(user, message):
	assert message_share_v1_request(user, message, "Hi", 12345, 12345).status_code == 400

def test_channel_and_dm_not_neg1(user, message, channel2, dm):
	assert message_share_v1_request(user, message, "Hi", channel2, dm).status_code == 400

def test_invalid_message(user, channel1):
	assert message_share_v1_request(user, 12345, "Hi", channel1).status_code == 400

def test_too_long(user, channel1, message):
	assert message_share_v1_request(user, message, "a" * 1000, channel1, -1).status_code == 200
	assert message_share_v1_request(user, message, "a" * 1001, channel1, -1).status_code == 400

def test_not_member_channel(user2, channel2, message):
	assert message_share_v1_request(user, message, "Hi", channel2, -1).status_code == 403

def test_not_member_dm(user, dm, message):
	assert message_share_v1_request(user, message, "Hi", -1, dm).status_code == 403

def test_shared_message_channel(user, channel2, message):
	assert message_share_v1_request(user, message, "Look at this idiot", channel2, -1).status_code == 200
	msg = channel_messages_v2_request(user, channel2, 0).json()['messages'][0]['message']
	assert "Look at this idiot" in msg
	assert "The world is flat" in msg

def test_shared_message_dm(user, dm, message):
	assert message_share_v1_request(user, message, "Truer words were never spoken", -1, dm).status_code == 200
	msg = dm_messages_v1_request(user, dm, 0),json()['messages'][0]['message']
	assert "Truer words were never spoken" in msg
	assert "The world is flat" in msg