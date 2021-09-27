from src.error import AccessError, InputError
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

# Returns true if channel_id refers to a valid channel, else false
def valid_channel_id(channel_id):
    store = data_store.get()
    channels = store['channels']
    for channel in channels:
        if channel['channel_id'] == channel_id:
            return True
    return False

# Returns true if u_id refers to a valid user, else false
def valid_user_id(u_id):
    store = data_store.get()
    users = store['users']
    for user in users:
        if user['u_id'] == u_id:
            return True
    return False

# Returns true if user u_id is a member of channel c_id, else false
def user_is_member(u_id, c_id):
    store = data_store.get()
    users = store['channels'][c_id]['users']

    for user in users:
        if user['u_id'] == u_id:
            return True
    return False


def channel_messages_v1(auth_user_id, channel_id, start):
    # Error cases
    if not valid_user_id(auth_user_id):
        raise AccessError("User ID does not belong to a user")

    if not valid_channel_id(channel_id):
        raise InputError("Channel does not exist")

    if not user_is_member(auth_user_id, channel_id):
        raise AccessError("User is not a member of the channel")
    
    store = data_store.get()
    messages = store['channels'][channel_id]['messages']

    if start > len(messages):
        raise InputError("Start must not be greater than the number of messages in the channel")
    
    # Get the up to 50 most recent messages from start
    page = messages[-(start + 1) : -(start + 51) : -1]

    end = (start + 50) if (start + 50) < len(messages) else -1

    return {
        'messages': page,
        'start': start,
        'end': end,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
