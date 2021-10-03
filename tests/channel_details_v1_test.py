import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1

@pytest.fixture(autouse=True)
def clear():
	clear_v1()


def test_invalid_channel_id():
    '''
    Test for invalid channel id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    with pytest.raises(InputError):
        assert channel_details_v1(u_id, 3)


def test_invalid_user_id():
    '''
    Test for valid channel id but invalid user id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    channel_id = channels_create_v1(u_id, "test channel", True)['channel_id']
    with pytest.raises(AccessError):
        assert channel_details_v1(-1, channel_id) 

def test_user_not_authorised():
    '''
    Test when channel_id is valid and the authorised user is not a member of the channel
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    u2_id = auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")['auth_user_id']
    channel_id = channels_create_v1(u_id, "test channel", True)['channel_id']
    with pytest.raises(AccessError):
        assert channel_details_v1(u2_id, channel_id)

def test_valid_channel_id():
    '''
    Test for valid channel id and user id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    channel_id = channels_create_v1(u_id, "test channel", True)['channel_id']
    channel_detail = {}
    channel_detail = channel_details_v1(u_id, channel_id)
    assert channel_detail == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
    }

def test_private_channel():
    '''
    Test for valid channel id and user id
    '''
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    channel_id = channels_create_v1(u_id, "test channel", False)['channel_id']
    channel_detail = {}
    channel_detail = channel_details_v1(u_id, channel_id)
    assert channel_detail == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'u_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
    }


def test_multiple_users():
    
    #Test when channel have multiple user and is private
    
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")['auth_user_id']
    u2_id = auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")['auth_user_id']
    u3_id = auth_register_v1("thirdemail@gmail.com", "password", "sam", "nguyen")['auth_user_id']

    channel_id = channels_create_v1(u_id, "test channel", True)['channel_id']
    channel_join_v1(u2_id, channel_id)
    channel_join_v1(u3_id, channel_id)
    channel_detail = {}

    channel_detail = channel_details_v1(u_id, channel_id)
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': u2_id ,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': u3_id ,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }
