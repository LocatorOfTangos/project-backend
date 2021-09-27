import pytest
import random
import time

from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1

# MISCELLANEOUS IMPORTS
from src.other import clear_v1
from src.error import InputError, AccessError


def successful_inv(is_public):
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PUBLIC INVITE FAILED' if is_public else\
                                                                        'PRIVATE INVITE FAILED'

    clear_v1


def test_successful_inv():
    successful_inv(True)
    successful_inv(False)


# DNE = DOES NOT EXIST
def test_uid_dne():
    inviter_id = auth_register_v1('inviter@email.com', 'password', 'mister', 'inviter')['auth_user_id']

    ls = list(range(2000, 2200, 20))
    dne_id = ls[random.randint(0, len(ls) - 1)]

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']

    with pytest.raises(InputError):
        assert channel_invite_v1(dne_id, channel_id, inviter_id), 'FAILED DNE_AUTH_UID TEST'
        assert channel_invite_v1(inviter_id, channel_id, dne_id), 'FAILED DNE_UID TEST' 


def test_invalid_channel_id():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    ls = list(range(2000, 2200, 20))
    dne_id = ls[random.randint(0, len(ls) - 1)]

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, dne_id, invited_id)


def test_access_error():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']

    with pytest.raises(AccessError):
        assert channel_invite_v1(invited_id, channel_id, invitee_id)