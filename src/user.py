from src.error import AccessError, InputError
from src.validation import valid_token, token_user, valid_user_id, get_user_details

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
