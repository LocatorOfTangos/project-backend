from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
import pytest

@pytest.fixture(autouse=True)
def clear():
	clear_v1()

def test_unique_names():
	correct_handles = {"blakemorris", "redmondmobbs", "vuluu"}

	# Create users
	u_id1 = auth_register_v1("user1@mail.com", "password", "blake", "morris")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "redmond", "mobbs")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "vu", "luu")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

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
	u_id1 = auth_register_v1("user1@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "qwertyuiopasdfg", "hjklzxcvbnm")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "mnbvcxzlkjhgfds", "apoiuytrewq")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

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
	u_id1 = auth_register_v1("user1@mail.com", "password", "blake", "morris")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "blake", "morris")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "blake", "morris")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

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
	u_id1 = auth_register_v1("user1@mail.com", "password", "bla&ke", "m#o&rr*is")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "r3d.....m0nd", "m0(b)b5")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "vu____", "l/u/u")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

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
	u_id1 = auth_register_v1("user1@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "abcdefghijklmnopq", "rstuvwxyz")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

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
	u_id1 = auth_register_v1("user1@mail.com", "password", "abcdefghijklmnopq", "rstabc")['auth_user_id']
	u_id2 = auth_register_v1("user2@mail.com", "password", "abcdefghijklmnopq", "rstdef")['auth_user_id']
	u_id3 = auth_register_v1("user3@mail.com", "password", "abcdefghijklmnopq", "rstghi")['auth_user_id']

	# Create channel
	c_id = channels_create_v1(u_id1, "channel", True)['channel_id']

	# Add users
	channel_join_v1(u_id2, c_id)
	channel_join_v1(u_id3, c_id)

	# Get members list
	membs = channel_details_v1(u_id1, c_id)['all_members']

	# Check handles are correct
	assert membs[0]['handle_str'] in correct_handles
	correct_handles.remove(membs[0]['handle_str'])
	
	assert membs[1]['handle_str'] in correct_handles
	correct_handles.remove(membs[1]['handle_str'])
	
	assert membs[2]['handle_str'] in correct_handles
	correct_handles.remove(membs[2]['handle_str'])