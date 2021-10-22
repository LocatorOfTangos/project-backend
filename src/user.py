from src.error import AccessError, InputError
from src.validation import valid_token, token_user, valid_user_id, get_user_details
from src.data_store import data_store

def user_profile_v1(token, u_id):
	'''
	Returns information about a user.

	Arguments:
		token (string)		- authorisation token of the user (session) requesting a profile
		u_id (int)			- u_id of the user to return the profile of

	Exceptions:
		InputError - Occurs when:
			> u_id does not refer to a valid user
		
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns a user dictionary containing 'u_id', 'email', 'name_first', 'name_last', 'handle_str'
	'''

	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not valid_user_id(u_id):
		raise InputError(description="Invalid u_id")

	return {'user': get_user_details(u_id)}

def user_profile_sethandle_v1(token, handle_str):
	'''
	Replaces the user's handle with handle_str.

	Arguments:
		token (string)		- authorisation token of the user (session) requesting a handle change
		handle_str (string) - new handle to use

	Exceptions:
		InputError - Occurs when:
			> u_id does not refer to a valid user
		
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns an empty dictionary
	'''

	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not 3 <= len(handle_str) <= 20:
		raise InputError(description="Handle must be between 3 and 20 characters")

	if not handle_str.isalnum():
		raise InputError(description="Handle must be alphanumeric")

	store = data_store.get()

	if any(u['handle_str'] == handle_str for u in store['users']):
		raise InputError(description="This handle is already in use")

	store['users'][token_user(token)]['handle_str'] = handle_str

	data_store.set(store)
	return {}