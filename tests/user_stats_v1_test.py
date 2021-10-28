import pytest
from src.make_request_test import *

# Reset application data before each test is run
@pytest.fixture(autouse=True)
def clear_data():
	clear_v1_request()

@pytest.fixture
def owner():
	return auth_register_v2_request("name1@email.com", "password", "firstname", "lastname").json()

@pytest.fixture
def member1():
	# Ensure user isn't global owner
	auth_register_v2_request("name2@email.com", "password", "firstname", "lastname")

	return auth_register_v2_request("name3@email.com", "password", "1firstname", "1lastname").json()

@pytest.fixture
def member2():
	# Ensure user isn't global owner
	auth_register_v2_request("name4@email.com", "password", "firstname", "lastname")

	return auth_register_v2_request("name5@email.com", "password", "2firstname", "2lastname").json()

@pytest.fixture
def channel1():
	member1 = auth_register_v2_request("namech1@email.com", "password", "firstname", "lastname").json()['token']
	return channels_create_v2_request(member1, "channel", True).json()['channel_id']

@pytest.fixture
def channel2():
	member1 = auth_register_v2_request("namech2@email.com", "password", "firstname", "lastname").json()['token']
	return channels_create_v2_request(member1, "channel", True).json()['channel_id']

def test_invalid_token():
	assert user_stats_v1_request('mentlegen').status_code == 403

def test_return_type_simple(member1):
    resp = user_stats_v1_request(member1).json()
    assert isinstance(resp, dict)
    
