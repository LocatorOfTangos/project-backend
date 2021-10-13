import pytest

from src.make_request import *

@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_test()

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_users_clear():
	# Successfully register and login a user
	user = auth_register_v2_test("user@mail.com", "password", "first", "last").json()
	assert auth_login_v2_test("user@mail.com", "password").json() == user

	clear_v1_test()

	assert auth_login_v2_test("user@mail.com", "password").status_code == 400

#@pytest.mark.skip(reason="Requires unimplemented functions")
def test_channels_clear():
	# Successfully register and login a user
	user = auth_register_v2_test("user@mail.com", "password", "first", "last").json()
	assert auth_login_v2_test("user@mail.com", "password").json() == user

	# Successfully create a channel and get its details
	channel = channels_create_v2_test(user['token'], "channel_name", True).json()
	assert channel_details_v2_test(user['token'], channel['channel_id']).status_code == 200

	clear_v1_test()

	assert channel_details_v2_test(user['token'], channel['channel_id']).status_code == 400

