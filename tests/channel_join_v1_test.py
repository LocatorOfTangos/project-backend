import pytest

from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Automatically applied to all tests
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1()

def test_return_type():
    user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")
    user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")

    channel_id = channels_create_v1(user1_id, "channelname", True)

    assert channel_join_v1(user2_id, channel_id) == {}

def test_invalid_channel_id():
    user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")

    # No channels to join
    with pytest.raises(InputError):
        assert channel_join_v1(user1_id, 0)

    user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")
    channels_create_v1(user1_id, "channelname", True)

    # A channel exists but the given channel_id is invalid
    with pytest.raises(InputError):
        assert channel_join_v1(user2_id, 9999999999999999)
    
    with pytest.raises(InputError):
        assert channel_join_v1(user1_id, 9999999999999999)

def test_already_public_channel_member():
    user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")
    channel_id = channels_create_v1(user1_id, "channelname", True)

    # Channel creator attempts to rejoin
    with pytest.raises(InputError):
        assert channel_join_v1(user1_id, channel_id)

    user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")
    channel_join_v1(user2_id, channel_id)

    # Channel member attempts to rejoin
    with pytest.raises(InputError):
        assert channel_join_v1(user2_id, channel_id)

def test_already_private_channel_member():
    user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")
    channel1_id = channels_create_v1(user1_id, "channel1name", False)

    # Global Owner attempts to rejoin their own private channel
    with pytest.raises(InputError):
        assert channel_join_v1(user1_id, channel1_id)

    user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")
    channel2_id = channels_create_v1(user2_id, "channel2name", False)
    channel_join_v1(user1_id, channel2_id)

    # Global Owner attempts to rejoin a member's private channel
    with pytest.raises(InputError):
        assert channel_join_v1(user1_id, channel2_id)

def test_non_global_owner_joins_private_channel():
    user1_id = auth_register_v1("name1@email.com", "password", "firstname", "lastname")
    channel_id = channels_create_v1(user1_id, "channelname", False)

    user2_id = auth_register_v1("name2@email.com", "password", "firstname", "lastname")

    with pytest.raises(AccessError):
        assert channel_join_v1(user2_id, channel_id)