import pytest
import time
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

@pytest.fixture
def ch_owner():
    return auth_register_v2_request('u@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def user():
	# Register an unused user to ensure not global owner
	auth_register_v2_request('u1@mail.com', 'password', 'first', 'last')
	return auth_register_v2_request('u2@mail.com', 'password', 'first', 'last').json()['token']

@pytest.fixture
def ch_pub(ch_owner):
	return channels_create_v2_request(ch_owner, "public", True).json()['channel_id']

@pytest.fixture
def ch_priv(ch_owner):
	return channels_create_v2_request(ch_owner, "private", False).json()['channel_id']

@pytest.fixture
def message():
    return 'Hello! I sent this message in the past!'

def test_status_code(ch_owner, ch_pub, ch_priv, message):
    time_sent = int(time.time()) + 3

    assert message_sendlater_v1_request(ch_owner, ch_pub, message, time_sent).status_code == 200
    assert message_sendlater_v1_request(ch_owner, ch_priv, message, time_sent).status_code == 200

def test_invalid_token(ch_pub, ch_priv, message):
    time_sent = int(time.time()) + 3

    assert message_sendlater_v1_request('ch_owner', ch_pub, message, time_sent).status_code == 403
    assert message_sendlater_v1_request('ch_owner', ch_priv, message, time_sent).status_code == 403

def test_invalid_channel_id(ch_owner, message):
    time_sent = int(time.time()) + 3

    assert message_sendlater_v1_request(ch_owner, 490234, message, time_sent).status_code == 400

def test_message_too_long(ch_owner, ch_pub, ch_priv):
    time_sent = int(time.time()) + 3
    message = 'a' * 1001

    assert message_sendlater_v1_request(ch_owner, ch_pub, message, time_sent).status_code == 400
    assert message_sendlater_v1_request(ch_owner, ch_priv, message, time_sent).status_code == 400

def test_sent_in_the_past(ch_owner, ch_pub, ch_priv, message):
    time_sent = int(time.time()) - 10
    assert message_sendlater_v1_request(ch_owner, ch_pub, message, time_sent).status_code == 400
    assert message_sendlater_v1_request(ch_owner, ch_priv, message, time_sent).status_code == 400

def test_user_is_not_member(user, ch_pub, ch_priv, message):
    time_sent = int(time.time()) + 3

    assert message_sendlater_v1_request(user, ch_pub, message, time_sent).status_code == 403
    assert message_sendlater_v1_request(user, ch_priv, message, time_sent).status_code == 403

def test_message_u_id(ch_owner, ch_pub, message):
    time_sent = int(time.time())

    u_id = auth_login_v2_request('u@mail.com', 'password').json()['auth_user_id']
    message_sendlater_v1_request(ch_owner, ch_pub, message, time_sent)
    message = channel_messages_v2_request(ch_owner, ch_pub, 0).json()['messages'][0]

    assert message['u_id'] == u_id

def test_message_ids_unique_single_channel(ch_owner, ch_pub):
    time_sent = int(time.time())
    used_ids = set()

    m_id = message_sendlater_v1_request(ch_owner, ch_pub, "m", time_sent).json()['message_id']
    assert m_id not in used_ids
    used_ids.add(m_id)
    m_id = message_sendlater_v1_request(ch_owner, ch_pub, "n", time_sent).json()['message_id']
    assert m_id not in used_ids
    used_ids.add(m_id)
    m_id = message_sendlater_v1_request(ch_owner, ch_pub, "o", time_sent).json()['message_id']
    assert m_id not in used_ids
    used_ids.add(m_id)
    m_id = message_sendlater_v1_request(ch_owner, ch_pub, "p", time_sent).json()['message_id']
    assert m_id not in used_ids
    used_ids.add(m_id)