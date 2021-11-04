import pytest
from src.make_request_test import *

@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

@pytest.fixture
def user():
	return auth_register_v2_request("u@m.com", "psword", "first", "last").json()

def test_invalid_token():
	assert user_profile_uploadphoto_v1_request('scarnoncunce', 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 0, 0).status_code == 403

def test_boundaries(user):
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 149, 149).status_code == 200
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 150, 150).status_code == 400
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 69, 0, 68, 1).status_code == 400
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 69, 1, 68).status_code == 400

def test_bad_url(user):
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://www.facebook.com/trololololol.JPG', 0, 0, 0, 0).status_code == 400
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://www.veryveryfakewebsitethatdoesntexist.com/blargh.JPG', 0, 0, 0, 0).status_code == 400

def test_bad_filetype(user):
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.PNG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 0, 0).status_code == 400
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.GIF/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 0, 0).status_code == 400

def test_successful(user):
    assert user_profile_uploadphoto_v1_request(user['token'], 'http://via.placeholder.com/150.JPG/FFFF00/000000/?text=UNSWstreamsPFP', 0, 0, 149, 149).status_code == 200

# TODO: improve test_successful, write further tests for additional data storage changes if possible