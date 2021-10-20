from src.data_store import data_store
from src.error import AccessError, InputError
from src.validation import valid_token, token_user, valid_channel_id, user_is_member
from datetime import datetime, timezone

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
	# Get the channel to send the messgae to
	store = data_store.get()
	channel = store['channels'][channel_id]

	# Assign a unique message_id
	message_id = store['curr_message_id']
	store['curr_message_id'] += 1

	# Add the message to the channel
	# Add to the front of the list due to channel/messages implementation
	channel['messages'][:0] = {
		'message_id': message_id,
		'u_id': u_id,
		'message': message,
		'time_created': datetime.now(timezone.utc).timestamp()
	}

	return {'message_id': message_id}


def message_send_v1(token, dm_id, message):
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

