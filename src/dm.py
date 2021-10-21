from src.error import InputError, AccessError
from src.validation import valid_token, valid_user_id, token_user
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


def dm_leave_v1(token, dm_id):
	store = data_store.get()

	if not valid_token(token):
		raise AccessError('Invalid token')

	for dm in store['dms']:
		if dm_id == dm['dm_id']:
			u_id = token_user(token)
			if u_id not in dm['all_members']:
				raise AccessError('dm_id is valid, but the authorised user is not a member of the DM.')

			dm['all_members'].remove(u_id)
			break

	else:
		raise InputError('dm_id does not refer to a valid DM.')

	return {}