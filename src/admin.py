from src.data_store import data_store
from src.error import AccessError, InputError
from src.validation import valid_token, valid_user_id, token_user 

def admin_userpermission_change_v1(token, u_id, permission_id):
	'''
	Given a valid owner token, updates a certain user's global permissions to those
	of an owner, or those of a member, as requested.

	Arguments:
		token (string) 		- token of the user requesting the change
		u_ids (int)	        - id of the user being affected
		permission_id (int) - global permission the user will be given

	Exceptions: 
		InputError - Occurs when:
			> u_id is invalid
			> permission_id is invalid
			> u_id refers to the only global owner who is being demoted
		AccessError - Occurs when:
			> token refers to a user who is not a global owner
			> token is invalid

	Return value:
		Returns an empty dictionary
	'''

	# Check that arguments are valid
	if not valid_token(token):
		raise AccessError(description='Invalid token')

	if not valid_user_id(u_id):
		raise InputError(description='Invalid u_id')

	if not (permission_id == 1 or permission_id == 2):
		raise InputError(description='Invalid permission_id')
	
	caller_id = token_user(token)

	store = data_store.get()

	num_owners = 0
	for user in store['users']:
		# Count the number of owners
		if user['global_permissions'] == 1:
			num_owners += 1
		# Raise AccessError if the caller is found not to be a global owner
		elif user['u_id'] == caller_id:
			raise AccessError(description='Caller must be a global owner')

	for user in store['users']:
		if user['u_id'] == u_id:
			# Raise an InputError if the caller is the last global owner and attempts to
			# demote themselves
			if u_id == caller_id and num_owners < 2 and permission_id == 2:
				raise InputError(description='A solitary owner cannot demote themselves')
			else:
				user['global_permissions'] = permission_id

	# Apply changes made to the store
	data_store.set(store)

	return {}
