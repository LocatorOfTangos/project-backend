import pytest

from src.make_request import *
from tests.helpers import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

def test_invalid_channel_id():
    '''
    Test for invalid channel id
    '''
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    assert channel_details_v2_request(u_id, 3).status_code == 400


def test_invalid_user_id():
    '''
    Test for valid channel id but invalid user id
    '''
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", True))['channel_id']
    assert channel_details_v2_request(-1, channel_id).status_code == 403

def test_user_not_authorised():
    '''
    Test when channel_id is valid and the authorised user is not a member of the channel
    '''
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    u2_id = resp_data(auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith"))['token']
    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", True))['channel_id']
    assert channel_details_v2_request(u2_id, channel_id).status_code == 403

def test_valid_channel_id():
    '''
    Test for valid channel id and user id
    '''
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", True))['channel_id']
    channel_detail = {}
    channel_detail = resp_data(channel_details_v2_request(u_id, channel_id))
    assert channel_detail == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': int(u_id),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(u_id) ,
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
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", False))['channel_id']
    channel_detail = {}
    channel_detail = resp_data(channel_details_v2_request(u_id, channel_id))
    assert channel_detail == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'u_id': int(u_id),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(u_id) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
    }


def test_multiple_users():

    #Test when channel have multiple user and is public

    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    u2_id = resp_data(auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith"))['token']
    u3_id = resp_data(auth_register_v2_request("thirdtestemail@gmail.com", "password", "sam", "nguyen"))['token']

    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", True))['channel_id']
    channel_join_v2_request(u2_id, channel_id)
    channel_join_v2_request(u3_id, channel_id)
    channel_detail = {}

    channel_detail = resp_data(channel_details_v2_request(u_id, channel_id))
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': int(u_id),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(u_id) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': int(u2_id) ,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': int(u3_id) ,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }

@pytest.mark.skip(reason="channel_invite_v2_request not implemented")
def test_multiple_users_priv():
    u_id = resp_data(auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu"))['token']
    u2_id = resp_data(auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith"))['token']
    u3_id = resp_data(auth_register_v2_request("thirdtestemail@gmail.com", "password", "sam", "nguyen"))['token']

    channel_id = resp_data(channels_create_v2_request(u_id, "test channel", False))['channel_id']
    channel_invite_v2_request(u_id, channel_id, u2_id)
    channel_invite_v2_request(u_id, channel_id, u3_id)
    channel_detail = {}

    channel_detail = resp_data(channel_details_v2_request(u_id, channel_id))
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'u_id': int(u_id),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(u_id) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': int(u2_id) ,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': int(u3_id) ,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }
