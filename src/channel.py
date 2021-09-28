from src.data_store import data_store
from src.error import InputError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    data = data_store.get()

    details = channel_details_v1(auth_user_id, channel_id)  # errors will be raised via channel_details

    if not any(u_id == user['u_id'] for user in data['users']) or any(u_id == user['u_id'] for user in details['all_members']):
        raise InputError

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(u_id)
            break

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
