import pytest

from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.validation import user_is_member

# Automatically applied to all tests
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1()

def test_invalid_user():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id = channels_create_v1(user1_id, "channelname", True)['channel_id']

	with pytest.raises(AccessError):
		channel_join_v1(1234569, channel_id)

def test_return_type():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']

	channel_id = channels_create_v1(user1_id, "channelname", True)['channel_id']

	assert channel_join_v1(user2_id, channel_id) == {}

# @pytest.mark.skip(reason="channel_details_v1 not functional")
def test_join_successful():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']

	pubchannel_id = channels_create_v1(user1_id, "channelname", True)['channel_id']
	channel_join_v1(user2_id, pubchannel_id)

	privchannel_id = channels_create_v1(user2_id, "privatechannelname", False)['channel_id']
	channel_join_v1(user1_id, privchannel_id)

	# A user can join a public server
	joined = False
	for user in channel_details_v1(user1_id, pubchannel_id)['all_members']:
		if user['u_id'] == user2_id:
			joined = True
			break
	
	assert joined == True

	# A global owner can join a private server
	joined = False
	for user in channel_details_v1(user2_id, privchannel_id)['all_members']:
		if user['u_id'] == user1_id:
			joined = True
			break
	
	assert joined == True

def test_join_public():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']

	pubchannel_id = channels_create_v1(user1_id, "channelname", True)['channel_id']
	channel_join_v1(user2_id, pubchannel_id)

	assert user_is_member(user1_id, pubchannel_id)
	assert user_is_member(user2_id, pubchannel_id)

def test_join_global_owner():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']

	privchannel_id = channels_create_v1(user2_id, "channelname", False)['channel_id']
	channel_join_v1(user1_id, privchannel_id)

def test_invalid_channel_id():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']

	# No channels to join
	with pytest.raises(InputError):
		assert channel_join_v1(user1_id, 0)

	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']
	channels_create_v1(user1_id, "channelname", True)

	# A channel exists but the given channel_id is invalid
	with pytest.raises(InputError):
		assert channel_join_v1(user2_id, 9999999999999999)
	
	with pytest.raises(InputError):
		assert channel_join_v1(user1_id, 9999999999999999)

def test_already_public_channel_member():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id = channels_create_v1(user1_id, "channelname", True)['channel_id']

	# Channel creator attempts to rejoin
	with pytest.raises(InputError):
		assert channel_join_v1(user1_id, channel_id)

	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel_join_v1(user2_id, channel_id)

	# Channel member attempts to rejoin
	with pytest.raises(InputError):
		assert channel_join_v1(user2_id, channel_id)

def test_already_private_channel_member():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel1_id = channels_create_v1(user1_id, "channel1name", False)['channel_id']

	# Global Owner attempts to rejoin their own private channel
	with pytest.raises(InputError):
		assert channel_join_v1(user1_id, channel1_id)

	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel2_id = channels_create_v1(user2_id, "channel2name", False)['channel_id']
	channel_join_v1(user1_id, channel2_id)

	# Global Owner attempts to rejoin a member's private channel
	with pytest.raises(InputError):
		assert channel_join_v1(user1_id, channel2_id)

def test_non_global_owner_joins_private_channel():
	user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id = channels_create_v1(user1_id, "channelname", False)['channel_id']

	user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")['auth_user_id']

	with pytest.raises(AccessError):
		assert channel_join_v1(user2_id, channel_id)