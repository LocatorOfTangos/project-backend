import pytest
from src.make_request_test import *
import time

def now():
    return int(time.time())

def time_eq(a, b):
    return abs(a - b) <= 1

@pytest.fixture(autouse=True)
def clear():
    clear_v1_request()


@pytest.fixture
def user():
    return auth_register_v2_request("u@mail.com", "psword", "first", "last").json()['token']


@pytest.fixture
def user2():
    return auth_register_v2_request("u2@mail.com", "psword", "first", "last").json()['token']


@pytest.fixture
def channel(user):
    return channels_create_v2_request(user, "channel", True).json()['channel_id']


def test_return_status(user, channel):
    assert standup_start_v1_request(user, channel, 60).status_code == 200

def test_time_finish(user, channel):
    assert time_eq(standup_start_v1_request(user, channel, 10).json()['finish_time'], now() + 10)
    assert time_eq(standup_start_v1_request(user, channel, 20).json()['finish_time'], now() + 20)
    assert time_eq(standup_start_v1_request(user, channel, 60).json()['finish_time'], now() + 60)
    assert time_eq(standup_start_v1_request(user, channel, 99999).json()['finish_time'], now() + 99999)

def test_not_member(channel, user2):
    assert standup_start_v1_request(user2, channel, 60).status_code == 403

def test_negative_start(user, channel):
    assert standup_start_v1_request(user, channel, 0).status_code == 200
    assert standup_start_v1_request(user, channel, -1).status_code == 400
    assert standup_start_v1_request(user, channel, -99999).status_code == 400

def test_invalid_channel(user):
    assert standup_start_v1_request(user, -999, 60).status_code == 400

def test_standup_already_active(user, channel):
    assert standup_start_v1_request(user, channel, 60).status_code == 200
    assert standup_start_v1_request(user, channel, 60).status_code == 400
    assert standup_start_v1_request(user, channel, 1).status_code == 400

def test_previous_standup_ended(user, channel):
    assert standup_start_v1_request(user, channel, 1).status_code == 200
    assert standup_start_v1_request(user, channel, 1).status_code == 400
    # Wait for first standup to end
    time.sleep(1.5)
    assert standup_start_v1_request(user, channel, 1).status_code == 200
    assert standup_start_v1_request(user, channel, 1).status_code == 400

def test_invalid_token(user, channel):
    assert standup_start_v1_request("qwerty", channel, 60).status_code == 403
    assert standup_start_v1_request("~" + user[1:], channel, 60).status_code == 403
    auth_logout_v1_request(user)
    assert standup_start_v1_request(user, channel, 60).status_code == 403

