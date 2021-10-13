import pytest
from src.error import InputError
from src.other import clear_v1

from tests.helpers import resp_comp
from src.make_request import *

# Reset application data before each test is run
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_test()

# Tests
def test_user_registered_1():
    user_reg = auth_register_v2_test("name@email.com", "password", "firstname", "lastname")
    user_log = auth_login_v2_test("name@email.com", "password")
    assert resp_comp(user_reg, user_log)

def test_user_registered_2():
    user_reg = auth_register_v2_test("imashellio@gmail.com", "99Blueballoons", "Redmond", "Mobbs")
    user_log = auth_login_v2_test("imashellio@gmail.com", "99Blueballoons")
    assert resp_comp(user_reg, user_log)

def test_multiple_users_registered():
    user1_reg = auth_register_v2_test("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty", "Ava", "Grenouille")
    user2_reg = auth_register_v2_test("Worrange@gmail.com", "7heReverend", "William", "Orange")
    user3_reg = auth_register_v2_test("haydensmith@outlook.com", "God1lovecomputerscience", "Hayden", "Smith")

    user2_log = auth_login_v2_test("Worrange@gmail.com", "7heReverend")
    user3_log = auth_login_v2_test("haydensmith@outlook.com", "God1lovecomputerscience")
    user1_log = auth_login_v2_test("Avagrenouille@funkymail.com", "h1pp1tyh0pp1ty")

    assert resp_comp(user1_reg, user1_log)
    assert resp_comp(user2_reg, user2_log)
    assert resp_comp(user3_reg, user3_log)

def test_unregistered_email():
    auth_register_v2_test("name@email.com", "password", "firstname", "lastname")
    assert auth_login_v2_test("name@squeemail.com", "password").status_code == 400

def test_no_registered_emails():
    assert auth_login_v2_test("boost@juicemail.com", "Mang0Mag1c").status_code == 400

def test_incorrect_password():
    auth_register_v2_test("JamisonFawkes@gigglemail.boom", "Junkrat", "Jamison", "Fawkes")
    auth_register_v2_test("TheEngineer@mercmail.tf", "PracticalProblems", "Dell", "Conagher")

    assert auth_login_v2_test("JamisonFawkes@gigglemail.boom", "Roadhog").status_code == 400
    assert auth_login_v2_test("TheEngineer@mercmail.tf", "ConundrumsOfPhilosophy").status_code == 400
