from src.data_store import data_store
from src.error import AccessError, InputError
from src.validation import *
from datetime import datetime, timezone
from src.user import stat_update, global_stat_update

def message_send_v1(token, channel_id, message):
	'''
	Sends a message to a channel (channel_id) from a user (token).
	The message is saved with a message_id, the u_id of the sender, the message contents and
	time_created as an integer Unix timestamp.

	Arguments:
		token (string)		- authorisation token of the user (session) sending the message
		channel_id (int)	- id of the channel to which the message is being sent
		message (string)	- contents of the message to send

	Exceptions:
		InputError - Occurs when:
			> channel_id does not refer to a valid channel
			> length of message is not 1..1000 characters (inclusive)
		
		AccessError - Occers when:
			> token is invalid
			> user is not a member of the (valid) channel

	Return Value:
		Returns a dictionary containing a unique integer 'message_id'
	'''
	### Error handling ###
	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not valid_channel_id(channel_id):
		raise InputError(description="Invalid channel_id")

	u_id = token_user(token)

	if not user_is_member(u_id, channel_id):
		raise AccessError(description="User is not a member of this channel")
	
	if not 1 <= len(message) <= 1000:
		raise InputError(description="Message length must be between 1 and 1000 chars (inclusive)")
	
	### Implementation ###

	# Update statistics
	stat_update(u_id, 'messages_sent', 1)
	global_stat_update('messages_exist', 1)

	# Get the channel to send the message to
	store = data_store.get()
	channel = store['channels'][channel_id]

	# Assign a unique message_id
	message_id = store['curr_message_id']
	store['curr_message_id'] += 1

	# Add the message to the channel
	# Add to the front of the list due to channel/messages implementation
	msg = {
		'message_id': message_id,
		'u_id': u_id,
		'message': message,
		'time_created': int(datetime.now(timezone.utc).timestamp()),
		'reacts': [{'react_id': 1, 'u_ids': []}],
		'is_pinned': False
	}

	channel['messages'].insert(0, msg)

	# Update the message info mapping
	store['message_info'][message_id] = {
		'type': 'channels',
		'sender': u_id,
		'to': channel_id
	}

	data_store.set(store)

	return {'message_id': message_id}


def message_senddm_v1(token, dm_id, message):
	'''
	Sends a message to a dm (dm_id) from a user (token).
	The message is saved with a message_id, the u_id of the sender, the message contents and
	time_created as an integer Unix timestamp.

	Arguments:
		token (string)		- authorisation token of the user (session) sending the message
		dm_id (int)			- id of the dm to which the message is being sent
		message (string)	- contents of the message to send

	Exceptions:
		InputError - Occurs when:
			> dm_id does not refer to a valid dm
			> length of message is not 1..1000 characters (inclusive)
		
		AccessError - Occers when:
			> token is invalid
			> user is not a member of the (valid) dm

	Return Value:
		Returns a dictionary containing a unique integer 'message_id'
	'''
	### Error handling ###
	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not valid_dm_id(dm_id):
		raise InputError(description="Invalid dm_id")

	u_id = token_user(token)

	if not user_is_member(u_id, dm_id, 'dms'):
		raise AccessError(description="User is not a member of this dm")
	
	if not 1 <= len(message) <= 1000:
		raise InputError(description="Message length must be between 1 and 1000 chars (inclusive)")
	
	### Implementation ###

	# Update statistics
	stat_update(u_id, 'messages_sent', 1)
	global_stat_update('messages_exist', 1)

	# Get the channel to send the messgae to
	store = data_store.get()
	dm = store['dms'][dm_id]

	# Assign a unique message_id
	message_id = store['curr_message_id']
	store['curr_message_id'] += 1

	# Add the message to the channel
	# Add to the front of the list due to channel/messages implementation
	msg = {
		'message_id': message_id,
		'u_id': u_id,
		'message': message,
		'time_created': int(datetime.now(timezone.utc).timestamp()),
		'reacts': [{'react_id': 1, 'u_ids': []}],
		'is_pinned': False
	}
	
	dm['messages'].insert(0, msg)

	# Update the message info mapping
	store['message_info'][message_id] = {
		'type': 'dms',
		'sender': u_id,
		'to': dm_id
	}

	data_store.set(store)

	return {'message_id': message_id}

def set_message_contents(message_id, to, chat_type, contents):
	store = data_store.get()
	for i, msg in enumerate(store[chat_type][to]['messages']):
		if msg['message_id'] == message_id:
			store[chat_type][to]['messages'][i]['message'] = contents
	data_store.set(store)

def remove_message(message_id, to, chat_type):
	# Update statistics
	global_stat_update('messages_exist', -1)

	store = data_store.get()
	for i, msg in enumerate(store[chat_type][to]['messages']):
		if msg['message_id'] == message_id:
			store[chat_type][to]['messages'].pop(i)
	data_store.set(store)

def message_edit_v1(token, message_id, message):
	'''
	Edits a message (message_id) to contain the text (message).
	If the new (message) is empty, the message is deleted.

	Arguments:
		token (string)		- authorisation token of the user (session) editing the message
		message_id (int)	- id of the message to edit
		message (string)	- contents of the message to replace previous version with

	Exceptions:
		InputError - Occurs when:
			> message_id does not refer to a valid message within a channel/dm that the user
			  has joined
			> length of message is more than 1000 characters
		
		AccessError - Occers when:
			> token is invalid
			> message_id is valid AND user is a member of the channel
			  AND message was not sent by the user AND user does not have owner permissions
			  in the channel

	Return Value:
		Returns an empty dictionary
	'''
	### Error handling ###
	
	if not valid_token(token):
		raise AccessError(description="Invalid token")

	u_id = token_user(token)

	store = data_store.get()
	
	# Get the message_id -> details mapping
	msgs = store['message_info']

	if message_id not in msgs.keys():
		raise InputError(description="Message does not exist")

	# Determine whether the message is in a channel or a dm
	chat_type = msgs[message_id]['type']
	
	# Determine the specific channel or dm the message is in
	to = msgs[message_id]['to']

	if not user_is_member(u_id, to, chat_type):
		raise InputError(description="Message does not exist")
	
	sender = msgs[message_id]['sender']

	# Access error if the user isn't either the sender of the message or a channel/global owner
	if not (sender == u_id or user_has_owner_perms(u_id, to, chat_type)):
		raise AccessError(description="User does not have permission to edit this message")
	
	if len(message) > 1000:
		raise InputError(description="Message must not be over 1000 chars")

	### Implementation ###

	# If the new message is empty, the message is deleted
	if message == "":
		remove_message(message_id, to, chat_type)
		return {}

	set_message_contents(message_id, to, chat_type, message)

	return {}

def message_remove_v1(token, message_id):
	'''
	Removes a message (message_id) from a channel or dm.

	Arguments:
		token (string)		- authorisation token of the user (session) removing the message
		message_id (int)	- id of the message to remove

	Exceptions:
		InputError - Occurs when:
			> message_id does not refer to a valid message within a channel/dm that the user
			  has joined
		
		AccessError - Occers when:
			> token is invalid
			> message_id is valid AND user is a member of the channel
			  AND message was not sent by the user AND user does not have owner permissions
			  in the channel

	Return Value:
		Returns an empty dictionary
	'''
	if not valid_token(token):
		raise AccessError(description="Invalid token")

	u_id = token_user(token)

	store = data_store.get()
	
	# Get the message_id -> details mapping
	msgs = store['message_info']

	if message_id not in msgs.keys():
		raise InputError(description="Message does not exist")

	# Determine whether the message is in a channel or a dm
	chat_type = msgs[message_id]['type']
	
	# Determine the specific channel or dm the message is in
	to = msgs[message_id]['to']

	if not user_is_member(u_id, to, chat_type):
		raise InputError(description="Message does not exist")
	
	sender = msgs[message_id]['sender']

	# Access error if the user isn't either the sender of the message or a channel/global owner
	if not (sender == u_id or user_has_owner_perms(u_id, to, chat_type)):
		raise AccessError(description="User does not have permission to edit this message")
	
	# Remove the message from the chat
	remove_message(message_id, to, chat_type)

	# Remove the message from the message info mapping
	msgs.pop(message_id)

	data_store.set(store)
	return {}

def message_react_v1(token, message_id, react_id):
	'''
	Adds a reaction 'react_id' to the message 'message_id' from the authorised user.

	Arguments:
		token (string)		- authorisation token of the user (session) reacting to the message
		message_id (int)	- id of the message to react to
		react_id (int)		- id of the reaction type to add

	Exceptions:
		InputError - Occurs when:
			> message_id does not refer to a valid message within a channel/dm that the user
			  has joined
			> react_id does not refer to a valid react type - see the list 'valid_reacts' below
			> The user has already reacted to this message with this react_id
		
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns an empty dictionary
	'''
	valid_reacts = [1]

	# Error handling
	if not valid_token(token):
		raise AccessError(description="Token is invalid")

	if react_id not in valid_reacts:
		raise InputError(description="Invalid react ID")

	u_id = token_user(token)


	# Get the message_id -> details mapping
	store = data_store.get()
	msgs = store['message_info']

	if message_id not in msgs.keys():
		raise InputError(description="Message does not exist")

	# Determine whether the message is in a channel or a dm
	chat_type = msgs[message_id]['type']
	
	# Determine the specific channel or dm the message is in
	to = msgs[message_id]['to']

	if not user_is_member(u_id, to, chat_type):
		raise InputError(description="Message does not exist")

	if user_has_reacted(u_id, message_id, react_id):
		raise InputError(description="User has already reacted to this message with this react")

	# Implementation
	# Add the react to the message
	for i, msg in enumerate(store[chat_type][to]['messages']):
		if msg['message_id'] == message_id:
			store[chat_type][to]['messages'][i]['reacts'][i - 1]['u_ids'].append(u_id)
	data_store.set(store)

	return {}