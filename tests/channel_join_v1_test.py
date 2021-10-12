import pytest

from src.make_request import *
from src.channel import channel_details_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.validation import user_is_member
from tests.helpers import *

# Automatically applied to all tests
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_request()

@pytest.fixture
def member():
	return auth_register_v2_request("name1@email.com", "password", "firstname", "lastname").json()['token']

@pytest.fixture
def user():
	# Ensure user isn't global owner
	auth_register_v2_request("name2@email.com", "password", "firstname", "lastname")

	return auth_register_v2_request("name3@email.com", "password", "firstname", "lastname").json()['token']

@pytest.fixture
def channel(member):
	return channels_create_v2_request(member, "channel", True).json()['channel_id']

@pytest.fixture
def private(member):
	return channels_create_v2_request(member, "channel", False).json()['channel_id']


# tests


def test_invalid_user(channel):
	assert channel_join_v2_request(1234569, channel).status_code == 403

def test_return_type(user, channel):
	assert channel_join_v2_request(user, channel).json() == {}

@pytest.mark.skip(reason="channel_details_v2 not functional")
def test_join_successful(user, member, channel,):
	assert channel_join_v2_request(user, channel).status_code == 200

	# A user can join a public server
	joined = False
	for user in channel_details_v1(user1_id, pubchannel_id)['all_members']:
		if user['u_id'] == user2_id:
			joined = True
			break
	
	assert joined == True

@pytest.mark.skip(reason="channel_details_v2 not functional")
def test_join_public(user, member, channel):
	channel_join_v2_request(user, channel)

	# TODO use details to check if joined

def test_join_global_owner():
	global_owner = auth_register_v2_request("owner@email.com", "password", "firstname", "lastname").json()['token']
	user2 = auth_register_v2_request("user@mail.com", "password", "first", "last").json()['token']
	channel = channels_create_v2_request(user2, "channel", False).json()['channel_id']
	assert channel_join_v2_request(global_owner, channel).status_code == 200

	# TODO use details to check if joined

def test_invalid_channel_id(user):
	# No channels to join
	assert channel_join_v2_request(user, 0).status_code == 400

	user2 = auth_register_v2_request("name5@email.com", "password", "firstname", "lastname").json()['token']
	channels_create_v2_request(user2, "channelname", True)

	# A channel exists but the given channel_id is invalid
	assert channel_join_v2_request(user, 9999999999999999).status_code == 400

def test_already_public_channel_member(channel, member, user):
	# Channel creator attempts to rejoin
	assert channel_join_v2_request(member, channel).status_code == 400

	channel_join_v2_request(user, channel)

	# Channel member attempts to rejoin
	assert channel_join_v2_request(user, channel).status_code == 400

def test_already_private_channel_member():
	# Global Owner attempts to rejoin their own private channel
	global_owner = auth_register_v2_request("owner@email.com", "password", "firstname", "lastname").json()['token']
	channel = channels_create_v2_request(global_owner, "channel", False).json()['channel_id']

	assert channel_join_v2_request(global_owner, channel).status_code == 400

	user2 = auth_register_v2_request("name21@email.com", "password", "firstname", "lastname").json()['token']
	channel2 = channels_create_v2_request(user2, "channel2name", False).json()['channel_id']
	channel_join_v2_request(global_owner, channel2)

	# Global Owner attempts to rejoin a member's private channel
	assert channel_join_v2_request(global_owner, channel2).status_code == 400

	# Member attempts to rejoin their own private channel
	assert channel_join_v2_request(user2, channel2).status_code == 400

def test_non_global_owner_joins_private_channel(private, user):
	assert channel_join_v2_request(user, private).status_code == 403