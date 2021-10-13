import pytest
from src.make_request import *


@pytest.fixture(autouse=True)
def clear():
	clear_v1_request()

def test_unique_names():
	correct_handles = {"blakemorris", "redmondmobbs", "vuluu"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "blake", "morris").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "redmond", "mobbs").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "vu", "luu").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])

def test_long_names():
	correct_handles = {"abcdefghijklmnopqrst", "qwertyuiopasdfghjklz", "mnbvcxzlkjhgfdsapoiu"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "qwertyuiopasdfg", "hjklzxcvbnm").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "mnbvcxzlkjhgfds", "apoiuytrewq").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])

def test_same_names():
	correct_handles = {"blakemorris", "blakemorris0", "blakemorris1"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "blake", "morris").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "blake", "morris").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "blake", "morris").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])

def test_non_alnum():
	correct_handles = {"blakemorris", "r3dm0ndm0bb5", "vuluu"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "bla&ke", "m#o&rr*is").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "r3d.....m0nd", "m0(b)b5").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "vu____", "l/u/u").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])

def test_long_duplicate_names():
	correct_handles = {"abcdefghijklmnopqrst", "abcdefghijklmnopqrst0", "abcdefghijklmnopqrst1"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])

def test_duplicate_after_truncate():
	correct_handles = {"abcdefghijklmnopqrst", "abcdefghijklmnopqrst0", "abcdefghijklmnopqrst1"}

	# Create users
	u_id1 = auth_register_v2_request("user1@mail.com", "password", "abcdefghijklmnopq", "rstabc").json()['token']
	u_id2 = auth_register_v2_request("user2@mail.com", "password", "abcdefghijklmnopq", "rstdef").json()['token']
	u_id3 = auth_register_v2_request("user3@mail.com", "password", "abcdefghijklmnopq", "rstghi").json()['token']

	# Create channel
	c_id = channels_create_v2_request(u_id1, "channel", True).json()['channel_id']

	# Add users
	channel_join_v2_request(u_id2, c_id)
	channel_join_v2_request(u_id3, c_id)

	# Get members list
	membs = channel_details_v2_request(u_id1, c_id).json()['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])