import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_listall_v1

# MISCELLANEOUS IMPORTS
from src.other import clear_v1
from src.error import AccessError


@pytest.fixture(autouse=True)
def clear():
    clear_v1()


def test_basic_listall():
    inviter_id = auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id']
    channels_create_v1(inviter_id, 'The Funky Bunch', True)

    assert channels_listall_v1(inviter_id) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'The Funky Bunch',
            }
        ]
    }


def test_basic_mult_list():
    inviter_id1 = auth_register_v1("inviter1@email.com", "password", "mister", "inviter1")['auth_user_id']

    channels_create_v1(inviter_id1, 'The Funky Bunch', True)
    channels_create_v1(inviter_id1, 'The Wonky Bunch', True)
    channels_create_v1(inviter_id1, 'The Lanky Bunch', True)

    assert channels_listall_v1(inviter_id1) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'The Funky Bunch',
            },
            {
                'channel_id': 1,
                'name': 'The Wonky Bunch',
            },
            {
                'channel_id': 2,
                'name': 'The Lanky Bunch',
            }
        ]
    }

    inviter_id2 = auth_register_v1("inviter2@email.com", "password", "mister", "inviter2")['auth_user_id']
    channels_create_v1(inviter_id2, 'The Funky Bunch', True)
    channels_create_v1(inviter_id2, 'The Wonky Bunch', True)
    channels_create_v1(inviter_id2, 'The Lanky Bunch', True)

    assert channels_listall_v1(inviter_id1) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'The Funky Bunch',
            },
            {
                'channel_id': 1,
                'name': 'The Wonky Bunch',
            },
            {
                'channel_id': 2,
                'name': 'The Lanky Bunch',
            },
            {
                'channel_id': 3,
                'name': 'The Funky Bunch',
            },
            {
                'channel_id': 4,
                'name': 'The Wonky Bunch',
            },
            {
                'channel_id': 5,
                'name': 'The Lanky Bunch',
            }
        ]
    }


def test_private_channels():
    inviter_id = auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id']

    channels_create_v1(inviter_id, 'The Funky Bunch', False)
    channels_create_v1(inviter_id, 'The Wonky Bunch', True)
    channels_create_v1(inviter_id, 'The Lanky Bunch', False)

    assert channels_listall_v1(inviter_id) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'The Funky Bunch',
            },
            {
                'channel_id': 1,
                'name': 'The Wonky Bunch',
            },
            {
                'channel_id': 2,
                'name': 'The Lanky Bunch',
            }
        ]
    }


def test_basic_DNE_id():
    with pytest.raises(AccessError):
        channels_listall_v1(22302)
