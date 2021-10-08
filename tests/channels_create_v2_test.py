import pytest
from src.make_request import channels_create_v2_request, auth_register_v2_request, clear_v1_request
from tests.helpers import resp_data

# Clears existing data for all tests
@pytest.fixture(autouse=True)
def clear():
      clear_v1_request()

@pytest.fixture
def user():
      resp = auth_register_v2_request("player1@mail.com", "password", "firstname", "lastname")
      user = resp_data(resp)['token']
      return user


# Tests for valid input for channels_create_v2_request 

def test_channel_name_too_long(user):
      assert channels_create_v2_request(user, "anextremelylongchannelname", True).status_code == 400
            
def test_channel_name_too_short(user):
      assert channels_create_v2_request(user, "", True).status_code == 400

def test_invalid_auth_id():
      assert channels_create_v2_request(20, "channelname", True).status_code == 403

def test_invalid_too_long():
      assert channels_create_v2_request(23467895, "anextremelylongchannelname", True).status_code == 403

def test_invalid_too_short():
      assert channels_create_v2_request(23467895, "", True).status_code == 403

# Test for correct output

def test_channel_id_uniqueness(user):
      used_channel_ids = set()
      
      channel_id1 = resp_data(channels_create_v2_request(user, "firstchannel", True))['channel_id']
      used_channel_ids.add(channel_id1)

      channel_id2 = resp_data(channels_create_v2_request(user, "firstchannel", True))['channel_id']
      assert channel_id2 not in used_channel_ids
      used_channel_ids.add(channel_id2)

      channel_id3 = resp_data(channels_create_v2_request(user, "firstchannel", True))['channel_id']
      assert channel_id3 not in used_channel_ids


def test_success_200(user):
      assert channels_create_v2_request(user, "firstchannel", True).status_code == 200

def test_valid_integer_output(user):
      channel_id6 = resp_data(channels_create_v2_request(user, "firstchannel", True))['channel_id']
      assert isinstance(channel_id6, int)

@pytest.mark.skip(reason='channel_details_v2 not yet implemented')
def test_owner_in_channel_public(user):
      c_id = resp_data(channels_create_v2_request(user, "newchannel", True))['channel_id']

@pytest.mark.skip(reason='channel_details_v2 not yet implemented')
def test_owner_in_channel_private(user):
      c_id = resp_data(channels_create_v2_request(user, "newchannel", False))['channel_id']

@pytest.mark.skip(reason='channel_details_v2 not yet implemented')
def test_owner(user):
      c_id = resp_data(channels_create_v2_request(user, "newchannel", True))['channel_id']

      details = resp_data(channel_details_v2_request(user, c_id))
      owners = details['owner_members']
      members = details['all_members']

      # Find user in owner_members matching c_id TODO not blackbox, use token rather than u_id
      assert owners == [
            {
                  'u_id': u_id,
                  'email': 'user@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            }
      ]
      
      assert members == [
            {
                  'u_id': u_id,
                  'email': 'user@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            }
      ]

@pytest.mark.skip(reason='channel_details_v2, channel_join_v2 not yet implemented')
def test_owner_with_other_members():
      u_id1 = resp_data(auth_register_v2_request("user1@mail.com", "password", "first", "last"))['auth_user_id']
      c_id = channels_create_v2_request(u_id1, "newchannel", True)['channel_id']
      
      u_id2 = resp_data(auth_register_v2_request("user2@mail.com", "password", "blake", "morris"))['auth_user_id']
      channel_join_v2_request(u_id2, c_id)
      
      u_id3 = resp_data(auth_register_v2_request("user3@mail.com", "password", "redmond", "mobbs"))['auth_user_id']
      channel_join_v2_request(u_id3, c_id)

      details = resp_data(channel_details_v2_request(u_id1, c_id))
      owners = details['owner_members']
      members = details['all_members']

      # Find user in owner_members matching c_id
      assert owners == [
            {
                  'u_id': u_id1,
                  'email': 'user1@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            }
      ]
      
      assert members == [
            {
                  'u_id': u_id1,
                  'email': 'user1@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            },
            {
                  'u_id': u_id2,
                  'email': 'user2@mail.com',
                  'name_first': 'blake',
                  'name_last': 'morris',
                  'handle_str': 'blakemorris'
            },
            {
                  'u_id': u_id3,
                  'email': 'user3@mail.com',
                  'name_first': 'redmond',
                  'name_last': 'mobbs',
                  'handle_str': 'redmondmobbs'
            }
      ]

@pytest.mark.skip(reason='channel_details_v2, channel_invite_v2 not yet implemented')
def test_owner_with_other_members_private():
      u_id1 = resp_data(auth_register_v2_request("user1@mail.com", "password", "first", "last"))['auth_user_id']
      c_id = resp_data(channels_create_v2_request(u_id1, "newchannel", False))['channel_id']
      
      u_id2 = resp_data(auth_register_v2_request("user2@mail.com", "password", "blake", "morris"))['auth_user_id']
      channel_invite_v2_request(u_id1, c_id, u_id2)
      
      u_id3 = resp_data(auth_register_v2_request("user3@mail.com", "password", "redmond", "mobbs"))['auth_user_id']
      channel_invite_v2_request(u_id1, c_id, u_id3)

      details = resp_data(channel_details_v2_request(u_id1, c_id))
      owners = details['owner_members']
      members = details['all_members']

      # Find user in owner_members matching c_id
      assert owners == [
            {
                  'u_id': u_id1,
                  'email': 'user1@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            }
      ]
      
      assert members == [
            {
                  'u_id': u_id1,
                  'email': 'user1@mail.com',
                  'name_first': 'first',
                  'name_last': 'last',
                  'handle_str': 'firstlast'
            },
            {
                  'u_id': u_id2,
                  'email': 'user2@mail.com',
                  'name_first': 'blake',
                  'name_last': 'morris',
                  'handle_str': 'blakemorris'
            },
            {
                  'u_id': u_id3,
                  'email': 'user3@mail.com',
                  'name_first': 'redmond',
                  'name_last': 'mobbs',
                  'handle_str': 'redmondmobbs'
            }
      ]