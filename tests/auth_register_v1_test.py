import pytest

from src.auth import auth_register_v1
from src.error import InputError

# Tests for invalid inputs:
def test_invalid_email():
	with pytest.raises(InputError):
	  	assert auth_register_v1("usermail.com", "password", "firstname", "lastname")
	
	with pytest.raises(InputError):
	  	assert auth_register_v1("user@mail", "password", "firstname", "lastname")
	
	with pytest.raises(InputError):
	  	assert auth_register_v1("@mail.com", "password", "firstname", "lastname")
	
	with pytest.raises(InputError):
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

def test_last_name_empty():
	with pytest.raises(InputError):
	  	assert auth_register_v1("firstname@mail.com", "password", "firstname", "")


