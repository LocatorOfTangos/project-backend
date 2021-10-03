import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.channels import channels_create_v1
from src.data_store import data_store

# MISCELLANEOUS IMPORTS
from src.other import clear_v1
from src.error import InputError, AccessError
from src.validation import user_is_member


@pytest.fixture(autouse=True)
def clear():
    clear_v1()


'''def successful_inv(is_public):
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', is_public)['channel_id']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PUBLIC INVITE FAILED' if is_public else\
                                                                        'PRIVATE INVITE FAILED'

    assert any(member['u_id'] == invited_id for member in channel_details_v1(inviter_id, channel_id)['all_members'])
'''

def test_successful_inv_public():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PUBLIC INVITE FAILED'
    assert user_is_member(invited_id, channel_id)


def test_successful_inv_private():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', False)['channel_id']
    assert channel_invite_v1(inviter_id, channel_id, invited_id) == {}, 'PRIVATE INVITE FAILED'
    assert user_is_member(invited_id, channel_id)


def test_multiple_members_invited():
    inviter_id, invited_id1, invited_id2 = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee1@email.com', 'password', 'mister', 'invited1')['auth_user_id'],
        auth_register_v1('invitee2@email.com', 'password', 'mister', 'invited2')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']
    assert channel_invite_v1(inviter_id, channel_id, invited_id1) == {}
    assert channel_invite_v1(inviter_id, channel_id, invited_id2) == {}

    assert user_is_member(invited_id1, channel_id)
    assert user_is_member(invited_id2, channel_id)
    #assert any(member['u_id'] == invited_id1 for member in channel_details_v1(inviter_id, channel_id)['all_members'])
    #assert any(member['u_id'] == invited_id2 for member in channel_details_v1(inviter_id, channel_id)['all_members'])

def test_invalid_auth_id():
    user_id = auth_register_v1('user@email.com', 'password', 'mister', 'user')['auth_user_id']
    channel_id = channels_create_v1(user_id, 'The Funky Bunch', True)['channel_id']

    with pytest.raises(AccessError):
        assert channel_invite_v1(1234, channel_id, user_id)

def test_invalid_invitee():
    user_id = auth_register_v1('user@email.com', 'password', 'mister', 'user')['auth_user_id']
    channel_id = channels_create_v1(user_id, 'The Funky Bunch', True)['channel_id']

    with pytest.raises(InputError):
        assert channel_invite_v1(user_id, channel_id, 1234)

def test_invalid_channel_id():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    dne_id = 2

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, dne_id, invited_id)


def test_already_member():
    inviter_id, invited_id = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee@email.com', 'password', 'mister', 'invited')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']
    channel_invite_v1(inviter_id, channel_id, invited_id)

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, invited_id)


def test_already_member_multiple():
    inviter_id, invited_id1, invited_id2 = (
        auth_register_v1("inviter@email.com", "password", "mister", "inviter")['auth_user_id'],
        auth_register_v1('invitee1@email.com', 'password', 'mister', 'invited1')['auth_user_id'],
        auth_register_v1('invitee2@email.com', 'password', 'mister', 'invited2')['auth_user_id']
    )

    channel_id = channels_create_v1(inviter_id, 'The Funky Bunch', True)['channel_id']
    channel_invite_v1(inviter_id, channel_id, invited_id1)
    channel_invite_v1(inviter_id, channel_id, invited_id2)

    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, invited_id1)
    with pytest.raises(InputError):
        assert channel_invite_v1(inviter_id, channel_id, invited_id2)


def test_inviter_not_a_member():
    channel_creator = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
    channel_id = channels_create_v1(channel_creator, "channel", True)['channel_id']

    inviter = auth_register_v1("user1@mail.com", "password", "first", "last")['auth_user_id']
    invitee = auth_register_v1("user2@mail.com", "password", "first", "last")['auth_user_id']

    with pytest.raises(AccessError):
        assert channel_invite_v1(inviter, channel_id, invitee)


def test_invite_transitivity():
    channel_creator = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
    channel_id = channels_create_v1(channel_creator, "channel", False)['channel_id']

    inviter = auth_register_v1("user1@mail.com", "password", "first", "last")['auth_user_id']
    invitee = auth_register_v1("user2@mail.com", "password", "first", "last")['auth_user_id']

    channel_invite_v1(channel_creator, channel_id, inviter)
    channel_invite_v1(inviter, channel_id, invitee)

    assert user_is_member(channel_creator, channel_id)
    assert user_is_member(inviter, channel_id)
    assert user_is_member(invitee, channel_id)