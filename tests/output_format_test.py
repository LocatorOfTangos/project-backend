import pytest
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1, channel_messages_v1
from src.other import clear_v1

@pytest.fixture(autouse=True)
def clear():
	clear_v1()

@pytest.fixture
def user():
	return auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']

@pytest.fixture
def user_2():
	return auth_register_v1("user2@mail.com", "password", "first", "last")['auth_user_id']

@pytest.fixture
def channel(user):
	return channels_create_v1(user, "channel", True)['channel_id']

@pytest.fixture
def priv_channel(user):
	return channels_create_v1(user, "channel", False)['channel_id']

def test_auth_register():
	out = auth_register_v1("user@mail.com", "password", "first", "last")
	assert isinstance(out, dict)
	assert set(out.keys()) == {'auth_user_id'}
	assert isinstance(out['auth_user_id'], int)

def test_auth_login(user):
	out = auth_login_v1("user@mail.com", "password")
	assert isinstance(out, dict)
	assert set(out.keys()) == {'auth_user_id'}
	assert isinstance(out['auth_user_id'], int)

def test_channels_create(user):
	out = channels_create_v1(user, "channel", True)
	assert isinstance(out, dict)
	assert set(out.keys()) == {'channel_id'}
	assert isinstance(out['channel_id'], int)

def test_channels_list_empty(user_2):
	out = channels_list_v1(user_2)
	assert isinstance(out, dict)
	assert set(out.keys()) == {'channels'}
	assert isinstance(out['channels'], list)

def test_channels_list_not_empty(user, channel, priv_channel):
	out = channels_list_v1(user)
	channel = out['channels'][0]
	assert isinstance(channel, dict)
	assert set(channel.keys()) == {'channel_id', 'name'}
	assert isinstance(channel['channel_id'], int)
	assert isinstance(channel['name'], str)
	assert len(out['channels']) == 1

def test_channels_listall_empty(user_2):
	out = channels_listall_v1(user_2)
	assert isinstance(out, dict)
	assert set(out.keys()) == {'channels'}
	assert isinstance(out['channels'], list)

def test_channels_listall_not_empty(user, channel, priv_channel):
	out = channels_listall_v1(user)
	channel = out['channels'][0]
	assert isinstance(channel, dict)
	assert set(channel.keys()) == {'channel_id', 'name'}
	assert isinstance(channel['channel_id'], int)
	assert isinstance(channel['name'], str)
	assert len(out['channels']) == 2

def test_channel_details(user, channel):
	out = channel_details_v1(user, channel)
	assert isinstance(out, dict)
	assert set(out.keys()) == {'name', 'is_public', 'owner_members', 'all_members'}
	assert isinstance(out['name'], str)
	assert isinstance(out['is_public'], bool)
	assert isinstance(out['owner_members'], list)
	assert isinstance(out['all_members'], list)
	
	own = out['owner_members'][0]
	assert isinstance(own, dict)
	assert set(own.keys()) == {'u_id', 'email', 'name_first', 'name_last', 'handle_str'}
	assert isinstance(own['u_id'], int)
	assert isinstance(own['email'], str)
	assert isinstance(own['name_first'], str)
	assert isinstance(own['name_last'], str)
	assert isinstance(own['handle_str'], str)

	memb = out['all_members'][0]
	assert isinstance(memb, dict)
	assert set(memb.keys()) == {'u_id', 'email', 'name_first', 'name_last', 'handle_str'}
	assert isinstance(memb['u_id'], int)
	assert isinstance(memb['email'], str)
	assert isinstance(memb['name_first'], str)
	assert isinstance(memb['name_last'], str)
	assert isinstance(memb['handle_str'], str)

def test_channel_join(user_2, channel):
	out = channel_join_v1(user_2, channel)
	assert isinstance(out, dict)
	assert len(out.keys()) == 0

def test_channel_invite(user, user_2, channel):
	out = channel_invite_v1(user, channel, user_2)
	assert isinstance(out, dict)
	assert len(out.keys()) == 0

def test_channel_messages(user, channel):
	out = channel_messages_v1(user, channel, 0)
	assert isinstance(out, dict)
	assert set(out.keys()) == {'messages', 'start', 'end'}
	assert isinstance(out['messages'], list)
	assert isinstance(out['start'], int)
	assert isinstance(out['end'], int)

	msgs = out['messages']
	assert len(msgs) == 0

def test_clear():
	out = clear_v1()
	assert isinstance(out, dict)
	assert len(out.keys()) == 0
