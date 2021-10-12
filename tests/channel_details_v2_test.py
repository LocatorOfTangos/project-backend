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
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    assert channel_details_v2_request(token, 3).status_code == 400


def test_invalid_user_id():
    '''
    Test for valid channel id but invalid user id
    '''
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    channel_id = channels_create_v2_request(token, "test channel", True).json()['channel_id']
    assert channel_details_v2_request(-1, channel_id).status_code == 403

def test_user_not_authorised():
    '''
    Test when channel_id is valid and the authorised user is not a member of the channel
    '''
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    token2 = auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith").json()['token']
    channel_id = channels_create_v2_request(token, "test channel", True).json()['channel_id']
    assert channel_details_v2_request(token2, channel_id).status_code == 403

def test_valid_channel_id():
    '''
    Test for valid channel id and user id
    '''
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    channel_id = channels_create_v2_request(token, "test channel", True).json()['channel_id']
    channel_detail = {}
    channel_detail = channel_details_v2_request(token, channel_id).json()
    assert channel_detail == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': int(token),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(token) ,
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
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    channel_id = channels_create_v2_request(token, "test channel", False).json()['channel_id']
    channel_detail = {}
    channel_detail = channel_details_v2_request(token, channel_id).json()
    assert channel_detail == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'u_id': int(token),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(token) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
    }


def test_multiple_users():

    #Test when channel have multiple user and is public

    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    token2 = auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith").json()['token']
    token3 = auth_register_v2_request("thirdtestemail@gmail.com", "password", "sam", "nguyen").json()['token']

    channel_id = channels_create_v2_request(token, "test channel", True).json()['channel_id']
    channel_join_v2_request(token2, channel_id)
    channel_join_v2_request(token3, channel_id)
    channel_detail = {}

    channel_detail = channel_details_v2_request(token, channel_id).json()
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': int(token),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(token) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': int(token2) ,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': int(token3) ,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }

@pytest.mark.skip(reason="channel_invite_v2_request not implemented")
def test_multiple_users_priv():
    token = auth_register_v2_request("testemail@gmail.com", "password", "vu", "luu").json()['token']
    token2 = auth_register_v2_request("secondtestemail@gmail.com", "password", "david", "smith").json()['token']
    token3 = auth_register_v2_request("thirdtestemail@gmail.com", "password", "sam", "nguyen").json()['token']

    channel_id = channels_create_v2_request(token, "test channel", False).json()['channel_id']
    channel_invite_v2_request(token, channel_id, token2)
    channel_invite_v2_request(token, channel_id, token3)
    channel_detail = {}

    channel_detail = channel_details_v2_request(token, channel_id).json()
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': False,
        'owner_members': [
            {
                'u_id': int(token),
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': int(token) ,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': int(token2) ,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': int(token3) ,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }
