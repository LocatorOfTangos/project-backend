from src.data_store import data_store


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
    channels = data_store.get()['channels']
    owners_channels = [{
        'channel_id': channel['channel_id'],
        'name': channel['name']
    } for channel in channels if auth_user_id in channel['owner_members']]

    return owners_channels


def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
