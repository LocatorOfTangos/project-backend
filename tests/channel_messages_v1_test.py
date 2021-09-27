import pytest

from src.channel import channel_messages_v1
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError

@pytest.fixture
def clear():
	clear_v1()

@pytest.fixture
def user():
	u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
	return u_id

@pytest.fixture
def channel(user):
	c_id = channels_create_v1(user, "channel", True)['channel_id'] # User automatically added to channel
	return c_id

def test_invalid_channel_id(clear, user, channel):
	with pytest.raises(InputError):
		assert channel_messages_v1(user, -1, 0)

	with pytest.raises(InputError):
		assert channel_messages_v1(user, 5, 0)

def test_valid_no_messages(clear, user, channel):
	assert channel_messages_v1(user, channel, 0) == {'messages': [], 'start':0, 'end':-1}

def test_invalid_user(clear, channel):
	with pytest.raises(AccessError):
		assert channel_messages_v1(12365478, channel, 0)

def test_invalid_start(clear, user, channel):
	with pytest.raises(InputError):
		assert channel_messages_v1(user, channel, 5)

def test_not_member(clear, channel):
	user_unauthorised = auth_register_v1("user2@mail.com", "password", "first", "last")['auth_user_id']
	with pytest.raises(AccessError):
		assert channel_messages_v1(user_unauthorised, channel, 0)