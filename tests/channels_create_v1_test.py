import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Clears existing data for all tests
@pytest.fixture(autouse=True)
def clear():
	clear_v1()

# Tests for valid input for channels_create_v1 

def test_channel_name_too_long():
	auth_user_id = auth_register_v1("player1@mail.com", "password", "firstname", "lastname")['auth_user_id']
	with pytest.raises(InputError):
		assert channels_create_v1(auth_user_id, "anextremelylongchannelname", True)
		
def test_channel_name_too_short():
	auth_user_id2 = auth_register_v1("player2@mail.com", "password", "firstname", "lastname")['auth_user_id']
	with pytest.raises(InputError):
		assert channels_create_v1(auth_user_id2, "", True)

def test_invalid_auth_id():
	with pytest.raises(AccessError):
		assert channels_create_v1(20, "channelname", True)

# Test for correct output

def test_channel_id_uniqueness():
	used_channel_ids = set()

	auth_user_id3 = auth_register_v1("player3@mail.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id1 = channels_create_v1(auth_user_id3, "firstchannel", True)['channel_id']
	used_channel_ids.add(channel_id1)

	auth_user_id4 = auth_register_v1("player4@mail.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id2 = channels_create_v1(auth_user_id4, "firstchannel", True)['channel_id']

	assert channel_id2 not in used_channel_ids
	used_channel_ids.add(channel_id2)

	auth_user_id5 = auth_register_v1("player5@mail.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id3 = channels_create_v1(auth_user_id5, "firstchannel", True)['channel_id']

	assert channel_id3 not in used_channel_ids

def test_valid_integer_output():
	auth_user_id6 = auth_register_v1("player6@mail.com", "password", "firstname", "lastname")['auth_user_id']
	channel_id6 = channels_create_v1(auth_user_id6, "firstchannel", True)['channel_id']
	assert isinstance(channel_id6, int)

