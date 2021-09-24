import pytest

from src.auth import auth_register_v1
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

# Test for correct incrementing for channel id

    def test_channel_id_increment():
	    auth_user_id3 = auth_register_v1("player3@gmail.com", "player321", "firstname", "lastname")
	    auth_user_id4 = auth_Register_v1("player4@gmail.com", "player432", "firstname", "lastname")

	    channel_id_one = channels_create_v1(auth_user_id3, "firstchannel", True)
	    channel_id_two = channels_create_v1(auth_user_id4, "secondchannnel", True)

	    assert channel_id_one = 1
	    assert channel_id_two = 2



