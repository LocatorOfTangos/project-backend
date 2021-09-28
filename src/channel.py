from src.error import AccessError, InputError
from src.data_store import data_store
from src.validation import user_is_member, valid_user_id, valid_channel_id

def channel_invite_v1(auth_user_id, channel_id, u_id):
	return {
	}

def channel_details_v1(auth_user_id, channel_id):

	'''Raise input error for invalid channel id
	Raise access error if auth_user_id is not in the channel
	Create an empty list to store all members and owners.
	Loop through channels in data_store. Find the matching channel_id. Return that channel dict
	'''
	# Check if channel is valid
	if not valid_channel_id(channel_id):
		raise InputError("Channel does not exist")

	# Check if user is in the channel
	if not user_is_member(auth_user_id, channel_id):
		raise AccessError("User is not a member of the channel")	

	# Check if user is valid
	if not valid_user_id(auth_user_id):
		raise AccessError("User ID does not belong to a user")

	# Implement the function
	owner = []
	members = []
	store = data_store.get()
	channels = store['channels']
	for channel in data[channels]:
		if channel.get("channel_id") == channel_id:
			channel_name = channel.get('name')
			
				






    

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


