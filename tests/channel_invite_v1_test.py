import pytest
import time

from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1

# MISCELLANEOUS IMPORTS
from src.other import clear_v1
from src.error import InputError, AccessError


@pytest.fixture(autouse=True)
def clear():
    clear_v1()


def successful_inv(is_public):
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PUBLIC INVITE FAILED' if is_public else\
                                                                        'PRIVATE INVITE FAILED'


@pytest.mark.skip(reason="Requires unimplemented functions")
def test_successful_inv_public():
    successful_inv(True)


@pytest.mark.skip(reason="Requires unimplemented functions")
def test_successful_inv_private():
    successful_inv(False)


# DNE = DOES NOT EXIST
@pytest.mark.skip(reason="Requires unimplemented functions")
def test_uid_dne():
    inviter_id = auth_register_v1('inviter@email.com', 'password', 'mister', 'inviter')['auth_user_id']

    dne_id = 2

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']

    with pytest.raises(InputError):
        assert channel_invite_v1(dne_id, channel_id, inviter_id), 'FAILED DNE_AUTH_UID TEST'

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, dne_id), 'FAILED DNE_UID TEST' 


@pytest.mark.skip(reason="Requires unimplemented functions")
def test_invalid_channel_id():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    ls = list(range(2000, 2200, 20))
    dne_id = ls[random.randint(0, len(ls) - 1)]

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, dne_id, invited_id)


@pytest.mark.skip(reason="Requires unimplemented functions")
def test_access_error():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channels']

    with pytest.raises(AccessError):
        assert channel_invite_v1(invited_id, channel_id, invitee_id)