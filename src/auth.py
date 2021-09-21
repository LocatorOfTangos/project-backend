from src.data_store import data_store
from src.error import InputError
import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def remove_non_alnum(string):
    result = ''
    for ch in string:
        if ch.isalnum():
            result += ch
    return result

def create_handle(first, last):
    # Generate handle from first 20 alphanum characters
    store = data_store.get()
    users = store['users']
    handle = remove_non_alnum(first.lower() + last.lower())[:20]

    # Check if handle is taken
    occurrences = 0
    for user in users:
        if user['first_name'] == first and user['last_name'] == last:
            occurrences += 1
    
    # If taken, append with a number
    if occurrences > 0:
        handle += f"{occurrences - 1}"
    
    return handle

def email_is_unique(email):
    store = data_store.get()
    users = store['users']

    for user in users:
        if user['email'] == email:
            return False

    return True

def email_is_valid(email):
    pattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if re.fullmatch(pattern, email):
        return True
    else:
        return False

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()
    users = store['users'] # List of users, index = id

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
    handle = create_handle(name_first, name_last)
    id = len(users)

    users.append({
        'first_name': name_first,
        'last_name': name_last,
        'email': email,
        'password': password,
        'handle': handle
    })
    
    return {
        'auth_user_id': id,
    }
