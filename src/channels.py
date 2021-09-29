from src.data_store import data_store
from src.error import InputError, AccessError
from src.validation import valid_user_id


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
    if not valid_user_id(auth_user_id):
        raise AccessError("User ID does not exist")

    channels = data_store.get()['channels']
    owners_channels = {
        'channels' : [{
            'channel_id': channel['channel_id'],
            'name': channel['name']
        } for channel in channels if auth_user_id in channel['owner_members']]
    }

    return owners_channels


def channels_create_v1(auth_user_id, name, is_public):

    store = data_store.get()
    channels = store['channels']

    #Check for valid user_id
    if not valid_user_id(auth_user_id):
        raise AccessError("User ID does not exist")

    #Check for valid channel name
    if not 1 <= len(name) <= 20:
        raise InputError('Invalid Channel Name. Name must be between 1 to 20 characters')
    
    # Create channel_id
    channel_id = len(channels) + 1
    
    channels_details = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages': []
    }
    
    store['channels'].append(channels_details)
    
    return {
        'channel_id': channel_id,
    }

