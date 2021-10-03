import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Clears existing data for all tests
@pytest.fixture(autouse=True)
def clear():
    clear_v1()

# Tests for valid output for channels_list_v1_test.py

def test_channels_list_basic():
    user_1 = auth_register_v1("user1@gmail.com", "password1", "firstname", "lastname")['auth_user_id']
    channels_create_v1(user_1, "channel", True)

    assert channels_list_v1(user_1) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel',
            }
        ]
    }


def test_channels_list_multiple():
    user_1 = auth_register_v1("user1@gmail.com", "password1", "firstname", "lastname")['auth_user_id']
    user_2 = auth_register_v1("user2@gmail.com", "password2", "firstname", "lastname")['auth_user_id']

    channels_create_v1(user_1, "channel", True)
    channels_create_v1(user_1, "channel2", True)
    channels_create_v1(user_2, "channel3", True)
    channels_create_v1(user_2, "channel4", True)

    assert channels_list_v1(user_1) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel',
            },
            {
                'channel_id': 1,
                'name': 'channel2',
            }
        ]
    }

    assert channels_list_v1(user_2) == {
        'channels': [
            {
                'channel_id': 2,
                'name': 'channel3',
            },
            {
                'channel_id': 3,
                'name': 'channel4',
            }
        ]
    }

def test_channels_list_private():
    user_1 = auth_register_v1("user1@mail.com", "password", "first", "last")['auth_user_id']
    user_2 = auth_register_v1("user2@mail.com", "password", "first", "last")['auth_user_id']

    channel_1 = channels_create_v1(user_1, "channel1", False)['channel_id']
    channels_create_v1(user_1, "channel2", False)

    assert channels_list_v1(user_1) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel1'
            },
            {
                'channel_id': 1,
                'name': 'channel2'
            }
        ]
    }

    assert channels_list_v1(user_2) == {'channels': []}

    channel_invite_v1(user_1, channel_1, user_2)

    assert channels_list_v1(user_2) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel1'
            }
        ]
    }

# Tests for valid user ID
def test_invalid_auth_id():
	with pytest.raises(AccessError):
		assert channels_list_v1(1234)


