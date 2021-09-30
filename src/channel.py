<<<<<<< HEAD
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
=======
from src.error import AccessError, InputError
from src.data_store import data_store
from src.validation import user_is_member, valid_user_id, valid_channel_id

def channel_invite_v1(auth_user_id, channel_id, u_id):
	return {
	}
>>>>>>> origin/master


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
	'''
	Returns a page of messages from the channel matching channel_id.
	Returns up to 50 messages, starting from index 'start' (where 0
	is the most recent message sent to the channel).

	Arguments:
		auth_user_id (integer)	- id of the user making the request
		channel_id (integer)	- id of the channel to retrieve messages from
		start (integer)			- index of the first message to retrieve

	Exceptions:
		InputError  - Occurs when:
			> The channel does not exist
			> Start is greater than the number of messages in the channel
		AcessError	- Occurs when:
			> auth_user_id does not belong to a user
			> User is not a member of the channel

	Return Value:
		Returns a dictionary containing 'messages' (a list of the up to 50 messages),
		'start', and 'end' (start + 50, or -1 if the last message of the channel has been
		retrieved)
	'''

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
