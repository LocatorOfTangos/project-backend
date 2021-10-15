'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    # List of user dictionaries, indexed by ID
    # User contains: u_id, email, name_first, name_last, handle_str, global_permissions
    'users': [],

    # List of session_id's (integers)
    # Each corresponds with the session_id of an active token
    'sessions': [],

    # List of passwords, indexed by ID
    'passwords': [],

    # List of channel dictionaries, indexed by ID
    # Channel contains: channel_id, name, is_public, owner_members[], all_members[], messages[]
    # Owner_members and all_members are lists of u_id's
    # Messages is a list of message dictionaries
    #   Add messages to front of list - most recent message should be at index 0
    #   Message dictionaries contain: message_id, u_id, message, time_created
    'channels': []
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

