from src.data_store import data_store
from src.error import InputError
import re

def auth_login_v1(email, password):
	#Initialising lists
	email_registered = False
	user_list = data_store.get()['users']
	password_list = data_store.get()['passwords']

	#Loop through users to find one with matching email
	for user in user_list:
		if user['email'] == email:
			user_id = user['u_id']
			email_registered = True
			break

	#Raise InputError if no user if found with corresponding email
	if email_registered == False:
		raise InputError('No user is registered with this Email')
		
	#Raise InputError if password is incorrect
	if password_list[user_id] != password:
		raise InputError('Incorrect Password')

	return {
		'auth_user_id': user_id,
	}

# Returns a copy of 'string' with all non-alphanumeric characters removed
def remove_non_alnum(string):
	result = ''
	for ch in string:
		if ch.isalnum():
			result += ch
	return result

# Generates a unique handle for a user by concatenating first and last names
# Number appended to end to differentiate users with the same name
# Handle contains only alphanumeric characters
# Handle is truncated to 20 name characters, exluding number for duplicate names
def create_handle(first, last):
	# Generate handle from first 20 alphanum characters
	store = data_store.get()
	users = store['users']
	handle = remove_non_alnum(first.lower() + last.lower())[:20]

	# Check if handle is taken
	occurrences = 0
	for user in users:
		if user['name_first'] == first and user['name_last'] == last:
			occurrences += 1
	
	# If taken, append with a number
	if occurrences > 0:
		handle += f"{occurrences - 1}"
	
	return handle

# Returns true if email address has not yet been used by a registered user in the data store
def email_is_unique(email):
	store = data_store.get()
	users = store['users']

	for user in users:
		if user['email'] == email:
			return False

	return True

# Returns true if email address matches the format for a valid email address
def email_is_valid(email):
	pattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
	return True if re.fullmatch(pattern, email) else False

def auth_register_v1(email, password, name_first, name_last):
	'''
	Registers a user by adding them to the users list of the data store and assigning an ID

	Arguments:
		email (string)		- email address of the user being registered
		password (string)	- password of the user
		name_first (string)	- first name of the user
		name_last (string)	- last name of the user

	Exceptions:
		InputError  - Occurs when:
			> Email address has already been used by a registered user
			> Email does not match the format of a valid email address
			> First or last name is not between 1 and 50 characters long (inclusive)
			> Password is less than 6 characters long

	Return Value:
		Returns a dictionary containing 'auth_user_id'
	'''
	# Normalise case of names
	name_first = name_first.title()
	name_last = name_last.title()

	# Check if email is valid
	if not email_is_unique(email):
		raise InputError('Email has already been used to register a user')
	
	if not email_is_valid(email):
		raise InputError('Email is invalid')

	# Check if names are valid
	if not 1 <= len(name_first) <= 50:
		raise InputError('First name must be between 1 and 50 characters')
	
	if not 1 <= len(name_last) <= 50:
		raise InputError('Last name must be between 1 and 50 characters')

	# Check if password is valid
	if len(password) < 6:
		raise InputError('Password must not be less than 6 characters')

	# Add to users list in data store
	store = data_store.get()
	users = store['users'] # List of users, index = id

	handle = create_handle(name_first, name_last)
	u_id = len(users)

	users.append({
		'u_id': u_id,
		'email': email,
		'name_first': name_first,
		'name_last': name_last,
		'handle_str': handle,
	})

	# Add password to data store
	store['passwords'].append(password)
	
	data_store.set(store)
	
	return {
		'auth_user_id': u_id,
	}
