import pytest
from src.make_request_test import *
from datetime import datetime, timezone
from time import sleep

# Reset application data before each test is run
@pytest.fixture(autouse=True)
def clear_data():
    clear_v1_request()

@pytest.fixture
def owner():
    return auth_register_v2_request("name1@email.com", "password", "firstname", "lastname").json()

@pytest.fixture
def member1(owner):
    return auth_register_v2_request("name2@email.com", "password", "1firstname", "1lastname").json()

@pytest.fixture
def member2(owner):
    return auth_register_v2_request("name3@email.com", "password", "2firstname", "2lastname").json()

@pytest.fixture
def channel1(member1):
    return channels_create_v2_request(member1['token'], "channel1", True).json()['channel_id']

@pytest.fixture
def channel2(member2, member1):
    channel_id = channels_create_v2_request(member2['token'], "channel2", False).json()['channel_id']
    channel_invite_v2_request(member2['token'], channel_id, member1['auth_user_id'])
    return channel_id

@pytest.fixture
def channel3(owner, member1):
    channel_id = channels_create_v2_request(owner['token'], "channel3", True).json()['channel_id']
    channel_join_v2_request(member1['token'], channel_id)
    return channel_id

@pytest.fixture
def dm1(member1, owner):
    return dm_create_v1_request(member1['token'], [owner['auth_user_id']]).json()['dm_id']

@pytest.fixture
def dm2(member1, member2, owner):
    return dm_create_v1_request(member2['token'], [owner['auth_user_id'], member1['auth_user_id']]).json()['dm_id']

def test_invalid_token():
    assert users_stats_v1_request('mentlegen').status_code == 403

def test_return_type_simple(member1):
    resp = users_stats_v1_request(member1['token']).json()
    assert len(resp['workplace_stats']) == 4

def test_no_utilisation(owner):
    token = auth_register_v2_request("name0@email.com", "password", "firstname", "lastname").json()['token']
    assert users_stats_v1_request(token).json()['workplace_stats']['utilisation_rate'] == 0 
    
def test_utilisation_rate(owner):
    assert users_stats_v1_request(owner['token']).status_code == 200
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == 0

    ownerchannel = channels_create_v2_request(owner['token'], 'ownerchannel', False).json()['channel_id']
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == 1

    member1 = auth_register_v2_request("name2@email.com", "password", "1firstname", "1lastname").json()
    member2 = auth_register_v2_request("name3@email.com", "password", "2firstname", "2lastname").json()
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == (1/3)

    dm1 = dm_create_v1_request(member1['token'], [owner['auth_user_id'], member2['auth_user_id']]).json()['dm_id']
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == 1

    dm_leave_v1_request(member2['token'], dm1)
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == (2/3)

    dm_remove_v1_request(member1['token'], dm1)
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == (1/3)

    channel_leave_v1_request(owner['token'], ownerchannel)
    assert users_stats_v1_request(owner['token']).json()['workplace_stats']['utilisation_rate'] == 0

def test_time_records(owner, member1):
    time = []
    time.append(int(datetime.now(timezone.utc).timestamp()))
    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['channels_exist'] == [{'num_channels_exist': 0, 'time_stamp': time[0]}]
    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time[0]}]
    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['messages_exist'] == [{'num_messages_exist': 0, 'time_stamp': time[0]}]

    time.append(int(datetime.now(timezone.utc).timestamp()))
    channel_id = channels_create_v2_request(member1['token'], 'channel1', True).json()['channel_id']
    time.append(int(datetime.now(timezone.utc).timestamp()))
    dm_id = dm_create_v1_request(member1['token'], [owner['auth_user_id']]).json()['dm_id']

    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['channels_exist'] == [{'num_channels_exist': 0, 'time_stamp': time[0]},
        {'num_channels_exist': 1, 'time_stamp': time[1]}]
    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time[0]},
        {'num_dms_exist': 1, 'time_stamp': time[2]}]

    sleep(1)
    time.append(int(datetime.now(timezone.utc).timestamp()))
    message_id = message_send_v1_request(member1['token'], channel_id, 'Hello').json()['message_id']

    time.append(int(datetime.now(timezone.utc).timestamp()))
    message_send_v1_request(member1['token'], dm_id, 'Hello')

    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['messages_exist'] == [{'num_messages_exist': 0, 'time_stamp': time[0]},
        {'num_messages_exist': 1,  'time_stamp': time[3]}, 
        {'num_messages_exist': 2, 'time_stamp': time[4]}]

    time.append(int(datetime.now(timezone.utc).timestamp()))
    message_remove_v1_request(member1['token'], message_id)

    time.append(int(datetime.now(timezone.utc).timestamp()))
    dm_remove_v1_request(member1['token'], dm_id)

    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['messages_exist'] == [{'num_messages_exist': 0, 'time_stamp': time[0]},
        {'num_messages_exist': 1,  'time_stamp': time[3]}, 
        {'num_messages_exist': 2, 'time_stamp': time[4]},
        {'num_messages_exist': 1, 'time_stamp': time[5]}]

    assert users_stats_v1_request(member1['token']).json()['workplace_stats']['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time[0]},
        {'num_dms_exist': 1, 'time_stamp': time[2]},
        {'num_dms_exist': 0, 'time_stamp': time[6]}]