from src.data_store import data_store
from src.error import InputError, AccessError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):

    store = data_store.get()
    channels = store['channels']

    #Check for valid user_id
    users = store['users']
    
    for user in users:
        if user['u_id'] == u_id:
            return True
        else:
            raise AccessError('Invalid User ID')
    
    #Check for valid channel name
    if not 1 <= len(name) <= 20:
        raise InputError('Invalid Channel Name. Name must be between 1 to 20 characters')
    
    #Create channel_id
    number_of_channels = len(channels)
    
    channels_details = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages': ,
    }
    
    store['channels'].append(channels_details)
    
    return {
        'channel_id': channel_id,
    }
