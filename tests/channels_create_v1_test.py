import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError
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

# Test for correct output and incrementing of channel ids

def test_channel_id_one():
	auth_user_id3 = auth_register_v1("player3@mail.com", "password", "firstname", "lastname")['auth_user_id']
	assert channels_create_v1(auth_user_id3, "firstchannel", True) == {'channel_id': 0}

def test_channel_id_multiple():
	auth_user_id4 = auth_register_v1("player4@mail.com", "password", "firstname", "lastname")['auth_user_id']
	assert channels_create_v1(auth_user_id4, "firstchannel", True) == {'channel_id': 0}

	auth_user_id5 = auth_register_v1("player5@mail.com", "password", "firstname", "lastname")['auth_user_id']
	assert channels_create_v1(auth_user_id5, "secondchannnel", True) == {'channel_id': 1}

	auth_user_id6 = auth_register_v1("player6@mail.com", "password", "firstname", "lastname")['auth_user_id']
	assert channels_create_v1(auth_user_id6, "thirdchannel", True) == {'channel_id': 2}

	auth_user_id7 = auth_register_v1("player7@mail.com", "password", "firstname", "lastname")['auth_user_id']
	assert channels_create_v1(auth_user_id7, "fourthchannel", True) == {'channel_id': 3}