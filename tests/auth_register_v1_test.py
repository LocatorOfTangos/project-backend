import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.data_store import data_store
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

# Tests for handle generation

@pytest.fixture
def users():
	store = data_store.get()
	return store['users']

def test_handle_unique(users):
	id1 = auth_register_v1("user1@mail.com", "password", "firstname", "lastname")['auth_user_id']
	id2 = auth_register_v1("user2@mail.com", "password", "firstname", "lastname")['auth_user_id']
	id3 = auth_register_v1("user3@mail.com", "password", "firstname", "lastname")['auth_user_id']

	users[id1]['handle'] != users[id2]['handle'] != users[id3]['handle']

def test_handle_increment(users):
	id1 = auth_register_v1("user1@mail.com", "password", "firstname", "lastname")['auth_user_id']
	id2 = auth_register_v1("user2@mail.com", "password", "firstname", "lastname")['auth_user_id']
	id3 = auth_register_v1("user3@mail.com", "password", "firstname", "lastname")['auth_user_id']

	assert users[id1]['handle'] == 'firstnamelastname'
	assert users[id2]['handle'] == 'firstnamelastname0'
	assert users[id3]['handle'] == 'firstnamelastname1'

def test_handle_length(users):
	id = auth_register_v1("user@mail.com", "password", "abcdefghijklm", "nopqrstuvwxyz")['auth_user_id']
	assert len(users[id]['handle']) <= 20

def test_handle_alphanumeric(users):
	id = auth_register_v1("user@mail.com", "password", "abc%^&$%&%^&$", "(^&def&%")['auth_user_id']
	assert users[id]['handle'].isalnum()