from src.error import AccessError, InputError
from src.data_store import data_store
from src.validation import user_is_member, valid_user_id, valid_channel_id, get_user_details

def channel_invite_v1(auth_user_id, channel_id, u_id):
	data = data_store.get()

	details = channel_details_v1(auth_user_id, channel_id)  # errors will be raised via channel_details

	if not any(u_id == user['u_id'] for user in data['users']):
		raise InputError('This user does not exist')

	if user_is_member(u_id, channel_id):
		raise InputError('This user has already been added to the channel')

	for channel in data['channels']:
		if channel['channel_id'] == channel_id:
			channel['all_members'].append(u_id)
			break

	return {
	}


def channel_details_v1(auth_user_id, channel_id):
	# Check if channel is valid
	if not valid_channel_id(channel_id):
		raise InputError("Channel does not exist")

	# Check if user is valid
	if not valid_user_id(auth_user_id):
		raise AccessError("User ID does not belong to a user")

	# Check if user is in the channel
	if not user_is_member(auth_user_id, channel_id):
		raise AccessError("User is not a member of the channel")	


	# Implement the function
	owners = []
	members = []
	channel_details = {}
	store = data_store.get()
	channels = store['channels']

	for channel in channels:

		# Find the channel_id in data_store
		if channel_id == channel['channel_id']:
			channel_name = channel.get('name')
			status = channel['is_public']

			# Add all members in channel list of all_members[] dictionary to members[] list
			# Use get_user_details function to get user's details 
			# from the data store.
			for user_member in channel['all_members']:
				temp_member = get_user_details(user_member)
				members.append(temp_member)

			# Add all owners in channel list of owner_member dictionary to owners[] list
			for user_owner in channel['owner_members']:
				temp_owner = get_user_details(user_owner)
				owners.append(temp_owner)

	channel_details = {
		'name': channel_name,
		'is_public': status,
		'owner_members': owners,
		'all_members': members,
	}

	return channel_details 



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

	if start < 0:
		raise InputError("Start must not be negative")
	
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
	store = data_store.get()
	users = store['users']
	channels = store['channels']
	joining_user = {}
	joining_channel = {}

	# Find user dictionary with corresponding u_id, raise AccessError if it does not exist
	for user in users:
		if user['u_id'] == auth_user_id:
			joining_user = user
			break
	if joining_user == {}:
		raise AccessError("User ID does not belong to a user")

	# Find channel dictionary with corresponding c_id, raise InputError if it does not exist
	for channel in channels:
		if channel['channel_id'] == channel_id:
			joining_channel = channel
			break
	if joining_channel == {}:
		raise InputError("Channel ID does not describe an existing channel")

	# Check whether user is already a member of the given channel, raise InputError if the case
	for member in joining_channel['all_members']:
		if member == auth_user_id:
			raise InputError("User is already a member of this channel")

	# Check if channel is private and user is not a global owner, raise AccessError if the case
	if joining_channel['is_public'] == False and joining_user['global_permissions'] != 1:
		raise AccessError("User does not have permissions to join channel")

	# Append user to the channel all_members list
	joining_channel['all_members'].append(joining_user['u_id'])
	
	return {}
