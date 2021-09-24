import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError
from src.other import clear_v1

# Clears existing data for all tests
@pytest.fixture(autouse=True)
def clear():
    clear_v1()

# Tests for valid output for channels_list_v1_test.py

def test_channels_list_v1():
    user_1 = auth_register_v1("user1@gmail.com", "password1", "firstname", "lastname")
    user_2 = auth_register_v1("user2@gmail.com", "password2", "firstname", "lastname")

    channels_create_v1(user_1, "channel", True)
    channels_create_v1(user_1, "channel2", True)
    channels_create_v1(user_2, "channel3", True)
    channels_create_v1(user_2, "channel4", True)

    assert channels_list_v1(user_1) == 
    {'channels': [
        {
            'id': 1,
            'name': 'channel',
        }
        {
            'id': 2,
            'name': 'channel2',
        }
    ]}

    assert channels_list_v1(user_2) == 
    {'channels': [
        {
            'id': 3,
            'name': 'channel3',
        }
        {
            'id': 4,
            'name': 'channel4',
        }
    ]}


