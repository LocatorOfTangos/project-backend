from src.data_store import data_store

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
    users = store['channels'][c_id]['all_members']

    for user in users:
        if user == u_id:
            return True
    return False