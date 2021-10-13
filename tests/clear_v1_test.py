import pytest

from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_request()

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_users_clear():
	# Successfully register and login a user
	user = auth_register_v2_request("user@mail.com", "password", "first", "last").json()
	assert auth_login_v2_request("user@mail.com", "password").json() == user

	clear_v1_request()

	assert auth_login_v2_request("user@mail.com", "password").status_code == 400

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_channels_clear():
	# Successfully register and login a user
	user = auth_register_v2_request("user@mail.com", "password", "first", "last").json()
	assert auth_login_v2_request("user@mail.com", "password").json() == user

	# Successfully create a channel and get its details
	channel = channels_create_v2_request(user['token'], "channel_name", True).json()
	assert channel_details_v2_request(user['token'], channel['channel_id']).status_code == 200

	clear_v1_request()

	assert channel_details_v2_request(user['token'], channel['channel_id']).status_code == 400

