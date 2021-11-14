import pytest
from src.auth import data_store
from src.validation import get_reset_code, reset_code_is_valid
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

def test_invalid_reset_code():
    assert auth_password_reset_v1_request(123, 'newpassword').status_code == 400
    assert auth_password_reset_v1_request(-1, 'newpassword').status_code == 400

def test_password_too_short():
    email = "testemail@gmail.com"
    u_id = auth_register_v2_request(email, "password", "firstname", "lastname").json()['auth_user_id']
    reset_code = get_reset_code(u_id)
    assert auth_password_reset_v1_request(reset_code, '123').status_code == 400

def test_valid_reset_code():
    email = "testemail@gmail.com"
    u_id = auth_register_v2_request(email, "password", "vu", "luu").json()['auth_user_id']
    auth_passwordreset_v1_request('testemail@gmail.com')
    reset_code = get_reset_code(u_id)
    assert auth_password_reset_v1_request(reset_code, 'newpassword').status_code == 200


    

    