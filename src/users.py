from src.error import AccessError, InputError
from src.validation import email_is_valid, valid_token, token_user, valid_user_id, get_user_details
from src.data_store import data_store

def users_all_v1(token):
	'''
	Returns information about all users.

	Arguments:
		token (string)		- authorisation token of the user (session) requesting a user list

	Exceptions:
		AccessError - Occers when:
			> token is invalid

	Return Value:
		Returns a list of users containing 'u_id', 'email', 'name_first', 'name_last', 'handle_str'
	'''
	if not valid_token(token):
		raise AccessError(description='Token is invalid')

	store = data_store.get()
	users = store['users']

	return {'users': [get_user_details(u['u_id']) for u in users if u['u_id'] != None]}