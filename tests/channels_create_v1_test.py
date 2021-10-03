import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.validation import user_is_member

# Clears existing data for all tests
@pytest.fixture(autouse=True)
def clear():
      clear_v1()

# Tests for valid input for channels_create_v1 

def test_channel_name_too_long():
      auth_user_id = auth_register_v1("player1@mail.com", "password", "firstname", "lastname")['auth_user_id']
      with pytest.raises(InputError):
            assert channels_create_v1(auth_user_id, "anextremelylongchannelname", True)
            
def test_channel_name_too_short():
      auth_user_id2 = auth_register_v1("player2@mail.com", "password", "firstname", "lastname")['auth_user_id']
      with pytest.raises(InputError):
            assert channels_create_v1(auth_user_id2, "", True)

def test_invalid_auth_id():
      with pytest.raises(AccessError):
            assert channels_create_v1(20, "channelname", True)

def test_invalid_too_long():
      with pytest.raises(AccessError):
            assert channels_create_v1(23467895, "anextremelylongchannelname", True)

def test_invalid_too_short():
      with pytest.raises(AccessError):
            assert channels_create_v1(23467895, "", True)

# Test for correct output

def test_channel_id_uniqueness():
      used_channel_ids = set()

      auth_user_id3 = auth_register_v1("player3@mail.com", "password", "firstname", "lastname")['auth_user_id']
      auth_user_id4 = auth_register_v1("player4@mail.com", "password", "firstname", "lastname")['auth_user_id']
      auth_user_id5 = auth_register_v1("player5@mail.com", "password", "firstname", "lastname")['auth_user_id']
      
      channel_id1 = channels_create_v1(auth_user_id3, "firstchannel", True)['channel_id']
      used_channel_ids.add(channel_id1)

      channel_id2 = channels_create_v1(auth_user_id4, "firstchannel", True)['channel_id']
      assert channel_id2 not in used_channel_ids
      used_channel_ids.add(channel_id2)

      channel_id3 = channels_create_v1(auth_user_id5, "firstchannel", True)['channel_id']
      assert channel_id3 not in used_channel_ids


def test_valid_integer_output():
      auth_user_id6 = auth_register_v1("player6@mail.com", "password", "firstname", "lastname")['auth_user_id']
      channel_id6 = channels_create_v1(auth_user_id6, "firstchannel", True)['channel_id']
      assert isinstance(channel_id6, int)

def test_owner_in_channel_public():
      u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
      c_id = channels_create_v1(u_id, "newchannel", True)['channel_id']
      assert user_is_member(u_id, c_id)

def test_owner_in_channel_private():
      u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
      c_id = channels_create_v1(u_id, "newchannel", False)['channel_id']
      assert user_is_member(u_id, c_id)

def test_owner():
      u_id = auth_register_v1("user@mail.com", "password", "first", "last")['auth_user_id']
      c_id = channels_create_v1(u_id, "newchannel", True)['channel_id']

      details = channel_details_v1(u_id, c_id)
      owners = details['owner_members']
      members = details['all_members']

      # Find user in owner_members matching c_id
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

def test_owner_with_other_members():
      u_id1 = auth_register_v1("user1@mail.com", "password", "first", "last")['auth_user_id']
      c_id = channels_create_v1(u_id1, "newchannel", True)['channel_id']
      
      u_id2 = auth_register_v1("user2@mail.com", "password", "blake", "morris")['auth_user_id']
      channel_join_v1(u_id2, c_id)
      
      u_id3 = auth_register_v1("user3@mail.com", "password", "redmond", "mobbs")['auth_user_id']
      channel_join_v1(u_id3, c_id)

      details = channel_details_v1(u_id1, c_id)
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

def test_owner_with_other_members_private():
      u_id1 = auth_register_v1("user1@mail.com", "password", "first", "last")['auth_user_id']
      c_id = channels_create_v1(u_id1, "newchannel", False)['channel_id']
      
      u_id2 = auth_register_v1("user2@mail.com", "password", "blake", "morris")['auth_user_id']
      channel_invite_v1(u_id1, c_id, u_id2)
      
      u_id3 = auth_register_v1("user3@mail.com", "password", "redmond", "mobbs")['auth_user_id']
      channel_invite_v1(u_id1, c_id, u_id3)

      details = channel_details_v1(u_id1, c_id)
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