import pytest

from src.other import clear_v1
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.error import InputError

@pytest.fixture(autouse=True)
def clear_data():
	clear_v1()

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_users_clear():
	# Successfully register and login a user
	user = auth_register_v1("user@mail.com", "password", "first", "last")
	assert auth_login_v1("user@mail.com", "password") == user

	clear_v1()

	with pytest.raises(InputError):
		assert auth_login_v1("user@mail.com", "password")

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_channels_clear():
	# Successfully register and login a user
	user = auth_register_v1("user@mail.com", "password", "first", "last")
	assert auth_login_v1("user@mail.com", "password") == user

	# Successfully create a channel and get its details
	channel = channels_create_v1(user['auth_user_id'], "channel_name", True)
	assert channel_details_v1(user['auth_user_id'], channel['channel_id'])['name'] == "channel_name"

	clear_v1()

	with pytest.raises(InputError):
		assert channel_details_v1(user['auth_user_id'], channel['channel_id'])['name']

