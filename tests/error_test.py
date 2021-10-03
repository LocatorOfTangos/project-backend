import pytest
from src.auth import *
from src.channel import *
from src.channels import *
from src.error import *
from src.other import *
from src.validation import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1()

@pytest.fixture
def valid_user():
	return auth_register_v1("user@mail.com", "password", "blake", "morris")['auth_user_id']

@pytest.fixture
def valid_channel(valid_user):
	return channels_create_v1(valid_user, "channel", True)

def test_all_invalid_auth(valid_user, valid_channel):
	with pytest.raises(AccessError):
		assert channels_create_v1(1234, "Channel", True)

	with pytest.raises(AccessError):
		assert channels_list_v1(1234)

	with pytest.raises(AccessError):
		assert channels_listall_v1(1234)

	with pytest.raises(AccessError):
		assert channel_details_v1(1234, valid_channel)

	with pytest.raises(AccessError):
		assert channel_join_v1(1234, valid_channel)

	with pytest.raises(AccessError):
		assert channel_invite_v1(1234, valid_channel, valid_user)

	with pytest.raises(AccessError):
		assert channel_messages_v1(1234, valid_channel, 0)

def test_error_precedence_channels_create():
	with pytest.raises(AccessError):
		# Create a channel with an invalid user AND name too short
		assert channels_create_v1(1234, "", True)

	with pytest.raises(AccessError):
		# Create a channel with an invalid user AND name too long
		assert channels_create_v1(1234, "hsjfgiowevkjhshbdfkgvhkewrhfvf", True)

def test_error_precedence_channel_details():
	with pytest.raises(AccessError):
		# Get channel details with an invalid user AND invalid channel id
		assert channel_details_v1(1234, 5678)

def test_error_precedence_channel_join():
	with pytest.raises(AccessError):
		# Join a channel an invalid user AND invalid channel id
		assert channel_details_v1(1234, 5678)

def test_error_precedence_channel_messages(valid_channel):
	with pytest.raises(AccessError):
		# Get messages with an invalid user AND invalid channel id
		assert channel_messages_v1(1234, 5678, 0)

	with pytest.raises(AccessError):
		# Get messages with an invalid user AND start > #messages
		assert channel_messages_v1(1234, valid_channel, 100)


	

