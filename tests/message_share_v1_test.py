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
def message(user, channel):
	return message_send_v1_request(user, channel, "The world is flat").json()['message_id']


def test_status(user, message, channel2):
	assert message_share_v1_request(user, message, "This guy agrees", channel2, -1).status_code == 200

def test_channel_and_dm_invalid(user, message):
	assert message_share_v1_request(user, message, "Hi", 12345, 12345).status_code == 400

def test_channel_and_dm_not_neg1(user, message, channel2, dm):
	assert message_share_v1_request(user, message, "Hi", channel2, dm).status_code == 400

def test_invalid_message(user, channel):
	assert message_share_v1_request(user, 12345, "Hi", channel).status_code == 400

def test_too_long(user, channel, message):
	assert message_share_v1_request(user, message, "a" * 1000, channel, -1).status_code == 200
	assert message_share_v1_request(user, message, "a" * 1001, channel, -1).status_code == 400

def test_not_member_channel(user2, channel2, message):
	assert message_share_v1_request(user, message, "Hi", channel2, -1).status_code == 403

def test_not_member_dm(user, dm, message):
	assert message_share_v1_request(user, message, "Hi", -1, dm).status_code == 403
