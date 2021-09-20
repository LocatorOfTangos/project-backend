import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

# Automatically applied to all tests
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1()

# Tests for valid registrations

def test_valid_register():
	register_return = auth_register_v1("user@mail.com", "password", "firstname", "lastname")
	login_return = auth_login_v1("user@mail.com", "password")
	assert register_return == login_return

def test_multiple_valid_registers():
	register1_return = auth_register_v1("user1@mail.com", "password", "firstname", "lastname")
	login1_return = auth_login_v1("user1@mail.com", "password")
	assert register1_return == login1_return

	register2_return = auth_register_v1("user2@mail.com", "password", "firstname", "lastname")
	login2_return = auth_login_v1("user2@mail.com", "password")
	assert register2_return == login2_return

def test_user_id_unique():
	used_ids = []
	for i in range(30):
		register_return = auth_register_v1(f"user{i}@mail.com", "password", "firstname", "lastname")
		assert register_return not in used_ids
		used_ids.append(register_return)

# Tests for invalid registrations

def test_invalid_email():
	with pytest.raises(InputError):
	  	assert auth_register_v1("usermail.com", "password", "firstname", "lastname")
	  	assert auth_register_v1("user@mail", "password", "firstname", "lastname")
	  	assert auth_register_v1("@mail.com", "password", "firstname", "lastname")
	  	assert auth_register_v1("user*@mail.com", "password", "firstname", "lastname")

def test_duplicate_email():
	auth_register_v1("user@mail.com", "password", "firstname", "lastname")
	with pytest.raises(InputError):
		auth_register_v1("user@mail.com", "password2", "firstname2", "lastname2")

def test_password_too_short():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "", "firstname", "lastname")

	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "12345", "firstname", "lastname")

def test_first_name_empty():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "password", "", "lastname")

def test_first_name_too_long():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "password", "a" * 51, "lastname")

def test_last_name_empty():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "password", "firstname", "")

def test_last_name_too_long():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "password", "firstname", "a" * 51)


