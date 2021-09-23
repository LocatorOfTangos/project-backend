import pytest

from src.other import clear_v1
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.error import InputError

def test_users_clear():
	clear_v1()
	u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
	clear_v1()
	with pytest.raises(InputError):
		assert auth_login_v1("user@mail.com", "password")

def test_channels_clear():
	clear_v1
	u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
	c_id = channels_create_v1(u_id, "channel", True)['channel_id']
	clear_v1()
	u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
	with pytest.raises(InputError):
		assert channel_details_v1(u_id, c_id)