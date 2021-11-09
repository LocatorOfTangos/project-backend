import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

def test_invalid_reset_code():
    assert auth_password_reset_v1(123, 'newpassword').status_code == 400
    assert auth_password_reset_v1(-1, 'newpassword').status_code == 400

def test_password_too_short():
    email = "testemail@gmail.com"
    auth_register_v2_request(email, "password", "vu", "luu")
    auth_passwordreset_request_v1('testemail@gmail.com')

    store = data_store.get()
    codes = store['reset_code']
    for code in codes:
        if code[email] == email:
            reset_code = code['reset_code']
            break

    assert auth_passwordreset_v1_request(reset_code, '123').status_code == 400


def test_valid_reset_code():
    email = "testemail@gmail.com"
    auth_register_v2_request(email, "password", "vu", "luu")
    auth_passwordreset_v1_request('testemail@gmail.com')

    store = data_store.get()
    codes = store['reset_code']
    for code in codes:
        if code[email] == email:
            reset_code = code['reset_code']
            break

    assert auth_passwordreset_v1_request(reset_code, 'newpassword').status_code == 200