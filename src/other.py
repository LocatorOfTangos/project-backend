from src.data_store import data_store

def clear_v1():
    '''
    Clears the data store to reset the state of the program

    No arguments
    No exceptions
    No return value
    '''

    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['passwords'] = []
    data_store.set(store)

    return {}