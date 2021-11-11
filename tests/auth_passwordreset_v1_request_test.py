import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

@pytest.fixture
def user():
    return auth_register_v2_request("user1@mail.com", "password", "firstname", "lastname").json()['token']

def test_invalid_email():
    assert auth_passwordreset_v1_request('a@mail.com').status_code == 400

#only works with auth_password_reset_v1
'''
def test_working_passwordreset_request(user):
    auth_passwordreset_v1_request('user1@mail.com')
    store = data_store.get()
    codes = store['reset_codes']
    for code in codes:
        if code['email'] == 'user1@mail.com':
            reset_code = code['reset_code']
            break

    assert auth_password_reset_v1(reset_code, 'user1@mail.com').status_code == 200
'''