import pytest

from tests.helpers import *
from src.make_request import *


@pytest.fixture(autouse=True)
def clear():
    clear_v1_request()

@pytest.fixture
def inviter():
    return auth_register_v2_request("inviter@email.com", "password", "mister", "inviter").json()['token']

@pytest.fixture
def public(inviter):
    return channels_create_v2_request(inviter, 'The Funky Bunch', True).json()['channel_id']

@pytest.fixture
def private(inviter):
    return channels_create_v2_request(inviter, 'The Funky Bunch', False).json()['channel_id']

@pytest.fixture
def invitee():
    return auth_register_v2_request('invitee@email.com', 'password', 'mister', 'invited').json()['token']

@pytest.fixture
def invitee2():
    return auth_register_v2_request('invitee2@email.com', 'password', 'mister', 'invited').json()['token']


def test_successful_inv_public(inviter, public, invitee):
    assert channel_invite_v2_request(inviter, public, invitee).status_code == 200
    # TODO: Check that they got added using channel_details


def test_successful_inv_private(inviter, private, invitee):
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 200
    # TODO: Check that they got added using channel_details

def test_multiple_members_invited(inviter, private, invitee, invitee2):
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 200
    assert channel_invite_v2_request(inviter, private, invitee2).status_code == 200
    # TODO: Check that they got added using channel_details

def test_invalid_auth_id(inviter, private, invitee):

    assert channel_invite_v2_request(1234, private, invitee).status_code == 403

def test_invalid_invitee(inviter, private):
    assert channel_invite_v2_request(inviter, private, 1234).status_code == 400

def test_invalid_channel_id(inviter, private, invitee):
    assert channel_invite_v2_request(inviter, 12356487, invitee).status_code == 400


def test_already_member(inviter, private, invitee):
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 200
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 400


def test_already_member_multiple(inviter, private, invitee, invitee2):
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 200
    assert channel_invite_v2_request(inviter, private, invitee2).status_code == 200

    assert channel_invite_v2_request(inviter, private, invitee).status_code == 400
    assert channel_invite_v2_request(inviter, private, invitee2).status_code == 400


def test_inviter_not_a_member(public, private, invitee, invitee2):
    assert channel_invite_v2_request(invitee, public, invitee2).status_code == 403
    assert channel_invite_v2_request(invitee, private, invitee2).status_code == 403


def test_invite_transitivity(inviter, private, invitee, invitee2):
    assert channel_invite_v2_request(invitee, private, invitee2).status_code == 403
    assert channel_invite_v2_request(inviter, private, invitee).status_code == 200
    assert channel_invite_v2_request(invitee, private, invitee2).status_code == 200
    # TODO: Check that they got added using channel_details