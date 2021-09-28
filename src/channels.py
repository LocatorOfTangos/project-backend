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
    
    #check if channel is public or private
    if is_public == True:
        public = True
    else:
        public = False
    
    #check for valid user_id
    users = store['users']
    
    '''
    might create a seperate file for these functions
    '''
    for user in users:
        if user['u_id'] == u_id:
            return True
        else:
            raise AccessError('User ID does not exist')
    
    #check for valid channel name
    if not 1 < len(name) < 20:
        raise InputError('Invalid Channel Name. Name must be between 1 to 20 characters')
    
    #create channel_id
    number_of_channels = len(channels)
    channel_id = number_of_channels + 1
    
    channels_details = {
        'channel_id': channel_id,
        'name': name,
        'is_public': public
        'owner_members': [auth_user_id]
        'all_members': [auth_user_id]
        'messages': ,
    }
    
    store['channels'].append(channels_details)
    
    return {
        'channel_id': channel_id,
    }
