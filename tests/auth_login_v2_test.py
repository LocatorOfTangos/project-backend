import pytest
from src.error import InputError
from src.other import clear_v1

from tests.helpers import resp_comp
from src.make_request import *

# Reset application data before each test is run
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_request()

# Tests
def test_user_registered_1():
    user_reg = auth_register_v2_request("name@email.com", "password", "firstname", "lastname")
    user_log = auth_login_v2_request("name@email.com", "password")
    assert resp_comp(user_reg, user_log)

def test_user_registered_2():
    user_reg = auth_register_v2_request("imashellio@gmail.com", "99Blueballoons", "Redmond", "Mobbs")
    user_log = auth_login_v2_request("imashellio@gmail.com", "99Blueballoons")
    assert resp_comp(user_reg, user_log)

def test_multiple_users_registered():
    user1_reg = auth_register_v2_request("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty", "Ava", "Grenouille")
    user2_reg = auth_register_v2_request("Worrange@gmail.com", "7heReverend", "William", "Orange")
    user3_reg = auth_register_v2_request("haydensmith@outlook.com", "God1lovecomputerscience", "Hayden", "Smith")

    user1_log = auth_login_v2_request("Worrange@gmail.com", "7heReverend")
    user2_log = auth_login_v2_request("haydensmith@outlook.com", "God1lovecomputerscience")
    user3_log = auth_login_v2_request("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty")

    assert resp_comp(user1_reg, user1_log)
    assert resp_comp(user2_reg, user2_log)
    assert resp_comp(user3_reg, user3_log)

def test_unregistered_email():
    auth_register_v2_request("name@email.com", "password", "firstname", "lastname")
    assert auth_login_v2_request("name@squeemail.com", "password").status_code == 400

def test_no_registered_emails():
    assert auth_login_v2_request("boost@juicemail.com", "Mang0Mag1c") == 400

def test_incorrect_password():
    auth_register_v2_request("JamisonFawkes@gigglemail.boom", "Junkrat", "Jamison", "Fawkes")
    auth_register_v2_request("TheEngineer@mercmail.tf", "PracticalProblems", "Dell", "Conagher")

    assert auth_login_v2_request("JamisonFawkes@gigglemail.boom", "Roadhog").status_code == 400
    assert auth_login_v2_request("TheEngineer@mercmail.tf", "ConundrumsOfPhilosophy").status_code == 400
