from src.error import AccessError, InputError
from src.data_store import data_store
from src.validation import user_is_member, valid_user_id, valid_channel_id

def channel_invite_v1(auth_user_id, channel_id, u_id):
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
    # Error cases
    if not valid_user_id(auth_user_id):
        raise AccessError("User ID does not belong to a user")

    if not valid_channel_id(channel_id):
        raise InputError("Channel does not exist")

    if not user_is_member(auth_user_id, channel_id):
        raise AccessError("User is not a member of the channel")
    
    store = data_store.get()
    messages = store['channels'][channel_id]['messages']

    if start > len(messages):
        raise InputError("Start must not be greater than the number of messages in the channel")
    
    # Get the up to 50 most recent messages from start
    page = messages[start : start + 50]

    # Get the index of the end of the page, or -1 if there are no messages after the page
    end = (start + 50) if (start + 50) < len(messages) else -1

    return {
        'messages': page,
        'start': start,
        'end': end,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
