#from data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    '''
    Raise input error for invalid channel id
    Raise access error if auth_user_id is not in the channel
    Create an empty list to store all members and owners.
    Loop through channels in data_store. Find the matching channel_id. Return that channel dict
    
    # Check if channel is valid
    if check_valid_channel(channel_id) == False:
        raise InputError("Invalid channel")
    
    # Check if user is in the channel
    
    # Implement the function
    '''


    

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

'''
def check_valid_channel(channel_id):

    # Loop through data_store to check if channel_id is present
    
    for channels in data_store['channels']:
        if channels.get('channel_id') == channel_id:
            return True           
    return False
'''
