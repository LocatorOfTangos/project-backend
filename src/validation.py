import jwt
import src.auth
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

# Returns the user id of the user associated with the token
# Assumes the token is valid
def token_user(token):
    return jwt.decode(token, src.auth.SECRET, algorithms=['HS256'])['u_id']

# Returns true if token refers to a valid user token
def valid_token(token):
    store = data_store.get()
    users = store['users']
    sessions = store['sessions']

    decoded_jwt = jwt.decode(token, src.auth.SECRET, algorithms=['HS256'])
    u_id = decoded_jwt['u_id']
    s_id = decoded_jwt['s_id']
    
    # Is the user valid?
    if not any(u['u_id'] == u_id for u in users):
        return False
    
    # Is the session valid?
    if not any(s == s_id for s in sessions):
        return False
    
    return True


# Returns true if user u_id is a member of channel c_id, else false
def user_is_member(u_id, c_id):
    store = data_store.get()
    users = store['channels'][c_id]['all_members']

    for user in users:
        if user == u_id:
            return True
    return False

# Return user's details as a dict given u_id
def get_user_details(u_id):
    store = data_store.get()
    users = store['users']
    user_details = {}
    for user in users:
        if user['u_id'] == u_id:
            user_details = {
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'email': user['email'],
                'handle_str': user['handle_str']

            }
    return user_details
