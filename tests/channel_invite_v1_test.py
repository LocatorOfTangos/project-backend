import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.channels import channels_create_v1
from src.data_store import data_store

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

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channel_id']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PUBLIC INVITE FAILED' if is_public else\
                                                                        'PRIVATE INVITE FAILED'

    assert any(member['u_id'] == invited_id for member in channel_details_v1(invited_id, channel_id)['all_members'])


def test_successful_inv_public():
    successful_inv(True)


def test_successful_inv_private():
    successful_inv(False)


# DNE = DOES NOT EXIST
def test_uid_dne():
    inviter_id = auth_register_v1('inviter@email.com', 'password', 'mister', 'inviter')['auth_user_id']

    dne_id = 2

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']

    with pytest.raises(InputError):
        assert channel_invite_v1(dne_id, channel_id, inviter_id), 'FAILED DNE_AUTH_UID TEST'

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, dne_id), 'FAILED DNE_UID TEST' 


def test_invalid_channel_id():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    dne_id = 2

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, dne_id, invited_id)


def test_member_exists():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']
    channel_invite_v1(inviter_id, channel_id, invited_id)

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, invited_id)


def test_access_error():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']

    with pytest.raises(AccessError):
        assert channel_invite_v1(invited_id, channel_id, invited_id)