import pytest

from src.other import clear_v1
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError

@pytest.fixture
def users():
	for i in range(20):
		auth_register_v1(f"user{i}@mail.com", f"password{i}", f"firstname{i}", f"lastname{i}")
	
def test_users_clear(users):
	# Check that users were added correctly
	for i in range(20):
		assert auth_login_v1(f"user{i}@mail.com", f"password{i}")['auth_user_id'] == i

	# Check that users get removed by clear
	clear_v1()
	for i in range(20):
		with pytest.raises(InputError):
	  		assert auth_login_v1(f"user{i}@mail.com", f"password{i}")

