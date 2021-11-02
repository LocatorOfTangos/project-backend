from src.error import InputError, AccessError
from src.data_store import data_store
from src.validation import token_user, valid_channel_id, valid_token, user_is_member
import threading
import time


def standup_timer(ch, length):
    store = data_store.get()

    # Initialise to an empty standup
    store['channels'][ch]['standup'] = {
        'is_active': True,
        'time_finish': int(time.time()) + length,
        'msg_queue': []
    }

    data_store.set(store)

    # Wait for the standup to end
    time.sleep(length)

    # Reset state of standup dict
    store['channels'][ch]['standup'] = {
        'is_active': False,
        'time_finish': None,
        'msg_queue': []
    }


def standup_start_v1(token, channel_id, length):
    '''
    Starts a standup in a channel for 'length' seconds
    During this time, messages are collated and sent at the end

    Arguments:
            token (string)		- authorisation token of the user (session) starting the standup
            channel_id (int)	- id of the channel in which the standup is ocurring
            length (int)	    - length in seconds of the standup

    Exceptions:
            InputError - Occurs when:
                    > channel_id does not refer to a channel
                    > length is negative
                    > a standup is already active in this channel

            AccessError - Occers when:
                    > token is invalid
                    > user is not a member of the (valid) channel

    Return Value:
            Returns a dictionary containing the time at which the standup will end
    '''
    if not valid_token(token):
        raise AccessError(description="Token is invalid")

    if not valid_channel_id(channel_id):
        raise InputError(description="Invalid channel ID")

    u_id = token_user(token)

    if not user_is_member(u_id, channel_id):
        raise AccessError(description="User is not a member of this channel")

    if length < 0:
        raise InputError(description="Length must not be negative")

    store = data_store.get()

    if store['channels'][channel_id]['standup']['is_active']:
        raise InputError(
            description="There is already an active standup in this channel")

    # Start the standup
    threading.Thread(target=standup_timer, args=[channel_id, length]).start()

    return {'time_finish': int(time.time()) + length}


def standup_active_v1(token, channel_id):
    '''
    Returns whether the channel has an active standup, and if so, when it will end.

    Arguments:
            token (string)		- authorisation token of the user (session) requesting information
            channel_id (int)	- id of the channel in which the standup is ocurring

    Exceptions:
            InputError - Occurs when:
                    > channel_id does not refer to a channel

            AccessError - Occers when:
                    > token is invalid
                    > user is not a member of the (valid) channel

    Return Value:
            Returns a dictionary containing whether there is a sstandup, and if so,
            the time at which the standup will end
    '''

    if not valid_token(token):
        raise AccessError(description="Token is invalid")

    if not valid_channel_id(channel_id):
        raise InputError(description="Invalid channel ID")

    u_id = token_user(token)

    if not user_is_member(u_id, channel_id):
        raise AccessError(description="User is not a member of this channel")

    store = data_store.get()

    return {
        'is_active': store['channels'][channel_id]['standup']['is_active'],
        'time_finish': store['channels'][channel_id]['standup']['time_finish']
    }