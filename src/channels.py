from src.data_store import data_store
from src.error import InputError, AccessError
from src.validation import valid_user_id

def channels_list_v1(auth_user_id):

    #check for valid user_id
    if not valid_user_id(auth_user_id):
        raise AccessError("User ID does not exist")
    
    #empty list for dictionary of channels
    list_channels = []

    #Loop through channel
    #Check if user is in channel, then append to channel list
    store = data_store.get()
    for channel in data_store['channels']:
        if user_id in channel['all_members']:
            list_channels.append({
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            })

    return {
        'channels': list_channels
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
    return {
        'channel_id': 1,
    }
