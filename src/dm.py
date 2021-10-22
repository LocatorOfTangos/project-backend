from src.error import InputError, AccessError
from src.validation import valid_token, valid_user_id, token_user, valid_channel_id
from src.data_store import data_store

def dm_create_v1(token, u_ids):
	'''
	Creates a new DM, owned by the authorised user and including the members referenced
	in u_ids.

	Arguments:
		token (string) 		- token of the user creating the dm
		u_ids (int list)	- ids of the users to add to the dm

	Exceptions:
		InputError  - Occurs when:
			> Any of the u_ids are invalid
		AccessError - Occurs when:
			> Token is invalid

	Return Value:
		Returns a dictionary containing the dm_id
	'''

	if not valid_token(token):
		raise AccessError(description='Invalid token')

	if any(not valid_user_id(u_id) for u_id in u_ids):
		raise InputError(description='One (or more) u_id is invalid')
	
	u_id = token_user(token)
	members = [u_id] + u_ids
	
	store = data_store.get()

	# Create dm_id
	dm_id = len(store['dms'])

	# Create name
	handles = sorted([store['users'][u]['handle_str'] for u in members])
	name = ', '.join(handles)

	dm_details = {
        'dm_id': dm_id,
        'name': name,
        'owner_members': [u_id],
		'all_members': members,
        'messages': []
    }
    
	store['dms'].append(dm_details)
    
    # Apply changes
	data_store.set(store)

	return {
	    'dm_id': dm_id,
	}


def dm_remove_v1(token, dm_id):
	store = data_store.get()

	if not valid_token(token):
		raise AccessError('Invalid token')

	if not valid_channel_id(dm_id, chat_type='dms'):
		raise InputError('dm_id does not refer to a valid DM.')

	u_id = token_user(token)
	if not valid_user_id(u_id):
		raise InputError('Not a valid u_id.')

	if u_id not in store['dms'][dm_id]['owner_members']:
		raise AccessError('dm_id is valid, but the authorised user is not an owner of the DM.')

	# Set to an empty channel
	store['dms'][dm_id] = {
		'dm_id': None,
		'name': 'Deleted',
		'owner_members': [],
		'all_members': [],
		'messages': []
	}

	data_store.set(store)

	return {}