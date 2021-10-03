import pytest 

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1

@pytest.fixture(autouse=True)
def clear():
	clear_v1()

def test():
    # Register and login
    auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    user_1 = auth_login_v1("testemail@gmail.com", "password")['auth_user_id']

    auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")
    user_2 = auth_login_v1("secondtestemail@gmail.com", "password")['auth_user_id']

    auth_register_v1("thirdtestemail@gmail.com", "password", "sam", "nguyen")
    user_3 = auth_login_v1("thirdtestemail@gmail.com", "password")['auth_user_id']

    # Create channels for testing
    channel_1 = channels_create_v1(user_1, "test channel", True)['channel_id']
    channel_2 = channels_create_v1(user_2, "test channel 2", True)['channel_id']
    channel_3 = channels_create_v1(user_3, "test channel 3", False)['channel_id']

    '''
    # Channel list
    assert channels_listall_v1(user_1) == {
        'channels': [
            {
                'channel_id': channel_1,
                'name': 'test channel',
            },
            {
                'channel_id': channel_2,
                'name': 'test channel 2',
            },
            {
                'channel_id': channel_3,
                'name': 'test channel 3',
            }
        ]
    }
    '''

    # Joining channel 1
    channel_join_v1(user_2, channel_1)
    channel_invite_v1(user_1, channel_1, user_3)

    assert channel_details_v1(user_1, channel_1) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'u_id': user_1,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
        ],
        'all_members': [
            {
                'u_id': user_1,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            },
            {
                'u_id': user_2,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': user_3,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ]
    }

    # Joining channel 2
    channel_invite_v1(user_2, channel_2, user_1)
    assert channel_details_v1(user_2, channel_2) == {
        'name': 'test channel 2',
        'is_public': True,
        'owner_members': [
            {
                'u_id': user_2,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
        ],
        'all_members': [
            {
                'u_id': user_2,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            },
            {
                'u_id': user_1,
                'name_first': 'vu',
                'name_last': 'luu',
                'email': 'testemail@gmail.com',
                'handle_str': 'vuluu'
            }
        ]
    }

    # Joining channel 3
    with pytest.raises(AccessError):
        assert channel_join_v1(user_2, channel_3)

    channel_invite_v1(user_3, channel_3, user_2)
    assert channel_details_v1(user_2, channel_3) == {
        'name': 'test channel 3',
        'is_public': False,
        'owner_members': [
            {
                'u_id': user_3,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
        ],
        'all_members': [
            {
                'u_id': user_3,
                'name_first': 'sam',
                'name_last': 'nguyen',
                'email': 'thirdtestemail@gmail.com',
                'handle_str': 'samnguyen'
            },
            {
                'u_id': user_2,
                'name_first': 'david',
                'name_last': 'smith',
                'email': 'secondtestemail@gmail.com',
                'handle_str': 'davidsmith'
            }
        ]
    }

    '''
    user_1 is in channel_1, channel_2
    user_2 is in channel_1, channel_2, channel_3
    user_3 is in channel_1, channel_3
    '''

    # Tests for channel_list
    assert channels_list_v1(user_1) == {
        'channels': [
            {
                'channel_id': channel_1,
                'name': 'test channel',
            },
            {
                'channel_id': channel_2,
                'name': 'test channel 2',
            }
        ]
    }

    assert channels_list_v1(user_2) == {
        'channels': [
            {
                'channel_id': channel_1,
                'name': 'test channel',
            },
            {
                'channel_id': channel_2,
                'name': 'test channel 2',
            },
            {
                'channel_id': channel_3,
                'name': 'test channel 3',
            }
        ]
    }

    assert channels_list_v1(user_3) == {
        'channels': [
            {
                'channel_id': channel_1,
                'name': 'test channel',
            },
            {
                'channel_id': channel_3,
                'name': 'test channel 3',
            }
        ]
    }

    
    



    



