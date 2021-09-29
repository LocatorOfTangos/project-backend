import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1

@pytest.fixture
def clear():
	clear_v1()

def test_invalid_channel_id():
    '''
    Test for invalid channel id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    with pytest.raises(InputError):
        assert(channel_details_v1(u_id, -1))

def test_invalid_user_id():
    '''
    Test for valid channel id but invalid user id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    channel_id = channels_create_v1(u_id, "test channel", True)
    with pytest.raises(InputError):
        assert(channel_details_v1(-1, channel_id))

@pytest.mark.skip(reason = "waiting for channels_create implementation")   
def test_valid_channel_id():
    '''
    Test for valid channel id and user id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    channel_id = channels_create_v1(u_id, "test channel", True)
    channel_detail = {}
    channel_detail = channel_details_v1(u_id, channel_id)
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'user_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
            },
        ],
        'all_members': [
            {
                'user_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
            },
        ],
    }

@pytest.mark.skip(reason = "waiting for channels_create implementation")
def test_user_not_authorised():
    '''
    Test when channel_id is valid and the authorised user is not a member of the channel
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    u2_id = auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")
    channel_id = channels_create_v1(u_id, "test channel", True)
    with pytest.raises(AccessError):
        assert(channel_details_v1(u2_id, channel_id))

@pytest.mark.skip(reason = "waiting for channels_create implementation")
def test_multiple_user():
    '''
    Test when channel have multiple user and is private
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    u2_id = auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")
    u3_id = auth_register_v1("thirdemail@gmail.com", "password", "sam", "nguyen")

    channel_id = channels_create_v1(u_id, "test channel", False)
    channel_join_v1(u2_id, channel_id)
    channel_join_v1(u3_id, channel_id)
    channel_detail = {}

    channel_detail = channel_details_v1(u_id, channel_id)
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'user_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
            },
        ],
        'all_members': [
            {
                'user_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
            },
            {
                'user_id': u2_id ,
                'name_first': 'david',
                'name_last': 'smith',
            },
            {
                'user_id': u3_id ,
                'name_first': 'sam',
                'name_last': 'nguyen',
            },
        ],








    
