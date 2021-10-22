from src.error import AccessError, InputError
from src.validation import email_is_valid, valid_token, token_user, valid_user_id, get_user_details
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

	if not valid_user_id(u_id, include_removed=True):
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
			> handle_str is not between 3 and 20 chars (inc.)
			> handle_str is already in use
			> handle_str is not entirely alphanumeric
		
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

def user_profile_setemail_v1(token, email):
	'''
	Replaces the user's email with email.

	Arguments:
		token (string)		- authorisation token of the user (session) requesting an email change
		email (string)		- new email to use

	Exceptions:
		InputError - Occurs when:
			> email is not a valid email format
			> email is already in use
		
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns an empty dictionary
	'''

	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not email_is_valid(email):
		raise InputError(description="Email does not match a valid format")

	store = data_store.get()

	if any(u['email'] == email for u in store['users']):
		raise InputError(description="This email is already in use")

	store['users'][token_user(token)]['email'] = email

	data_store.set(store)
	return {}

def user_profile_setname_v1(token, name_first, name_last):
	'''
	Replaces the user's first and last names.

	Arguments:
		token (string)		- authorisation token of the user (session) requesting an email change
		name_first (string)	- new first name to use
		name_last (string)	- new last name to use

	Exceptions:
		InputError - Occurs when:
			> either name is not 1..50 characters
		
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns an empty dictionary
	'''

	if not valid_token(token):
		raise AccessError(description="Invalid token")

	if not (1 <= len(name_first) <= 50 and 1 <= len(name_last) <= 50):
		raise InputError(description="Both names must be between 1 and 50 chars long (inc.)")

	store = data_store.get()

	store['users'][token_user(token)]['name_first'] = name_first
	store['users'][token_user(token)]['name_last'] = name_last

	data_store.set(store)
	return {}