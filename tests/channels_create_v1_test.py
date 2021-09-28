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
	auth_user_id = auth_register_v1("player1@gmail.com", "player123", "firstname", "lastname")
	with pytest.raises(InputError):
		assert channels_create_v1(auth_user_id, "anextremelylongchannelname" , True)
		
def test_channel_name_too_short():
	auth_user_id2 = auth_register_v1("player2@gmail.com", "player234", "firstname", "lastname")
	with pytest.raises(InputError):
		assert channels_create_v1(auth_user_id2 , " ", True)

# Test for correct output and incrementing of channel ids

def test_channel_id_one():
	auth_user_id3 = auth_register_v1("player3@gmail.com", "player321", "firstname", "lastname")
	assert channels_create_v1(auth_user_id3, "firstchannel", True) = 1

def test_channel_id_multiple():
	auth_user_id4 = auth_register_v1("player4@gmail.com", "player543", "firstname", "lastname")
	assert channels_create_v1(auth_user_id4, "firstchannel", True) = 1

	auth_user_id5 = auth_register_v1("player5@gmail.com", "player654", "firstname", "lastname")
	assert channels_create_v1(auth_user_id5, "secondchannnel", True) = 2

	auth_user_id6 = auth_register_v1("player6@gmail.com", "player765", "firstname", "lastname")
	assert channels_create_v1(auth_user_id6, "thirdchannel", True) = 3

	auth_user_id7 = auth_register_v1("player7@gmail.com", "player876", "firstname", "lastname")
	assert channels_create_v1(auth_user_id7, "fourthchannel", True) = 4