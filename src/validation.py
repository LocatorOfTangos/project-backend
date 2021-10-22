import jwt
import src.auth
from src.data_store import data_store
from src.error import AccessError

# Returns true if channel_id refers to a valid channel, else false
def valid_channel_id(channel_id, chat_type='channels'):
    store = data_store.get()
    channels = store[chat_type]
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

    try:
        decoded_jwt = jwt.decode(token, src.auth.SECRET, algorithms=['HS256']) 
    except Exception:
        return False

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
# if optional third arg is 'dms', checks dms instead of channels
def user_is_member(u_id, c_id, chat_type='channels'):
    store = data_store.get()
    users = store[chat_type][c_id]['all_members']

    for user in users:
        if user == u_id:
            return True
    return False

# Returns true if user u_id is a global owner and a member of the channel,
# or is an owner of the channel
# if optional third arg is 'dms', checks dms instead of channels
def user_has_owner_perms(u_id, c_id, chat_type='channels'):
    store = data_store.get()

    if store['users'][u_id]['global_permissions'] == 1 and user_is_member(u_id, c_id):
        return True

    if any(u == u_id for u in store[chat_type][c_id]['owner_members']):
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

