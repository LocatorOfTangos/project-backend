import pytest

from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
from src.other import clear_v1

# Reset application data before each test is run
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1()

# Tests
def test_user_registered_1():
    user_id = auth_register_v1("name@email.com", "password", "firstname", "lastname")
    assert auth_login_v1("name@email.com", "password") == user_id

def test_user_registered_2():
    user_id = auth_register_v1("imashellio@gmail.com", "99Blueballoons", "Redmond", "Mobbs")
    assert auth_login_v1("imashellio@gmail.com", "99Blueballoons") == user_id

def test_multiple_users_registered():
    user1_id = auth_register_v1("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty", "Ava", "Grenouille")
    user2_id = auth_register_v1("Worrange@gmail.com", "7heReverend", "William", "Orange")
    user3_id = auth_register_v1("haydensmith@outlook.com", "God1lovecomputerscience", "Hayden", "Smith")
    assert auth_login_v1("Worrange@gmail.com", "7heReverend") == user2_id
    assert auth_login_v1("haydensmith@outlook.com", "God1lovecomputerscience") == user3_id
    assert auth_login_v1("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty") == user1_id

def test_unregistered_email():
    auth_register_v1("name@email.com", "password", "firstname", "lastname")
    with pytest.raises(InputError):
        assert auth_login_v1("name@squeemail.com", "password")

def test_no_registered_emails():
    with pytest.raises(InputError):
        assert auth_login_v1("boost@juicemail.com", "Mang0Mag1c")

def test_incorrect_password():
    auth_register_v1("JamisonFawkes@gigglemail.boom", "Junkrat", "Jamison", "Fawkes")
    auth_register_v1("TheEngineer@mercmail.tf", "PracticalProblems", "Dell", "Conagher")

    with pytest.raises(InputError):
        assert auth_login_v1("JamisonFawkes@gigglemail.boom", "Roadhog")

    with pytest.raises(InputError):
        assert auth_login_v1("TheEngineer@mercmail.tf", "ConundrumsOfPhilosophy")