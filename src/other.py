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
    store['sessions'] = []
    store['channels'] = []
    store['passwords'] = []
    store['curr_channel_id'] = 0
    store['curr_session_id'] = 0
    data_store.set(store)

    return {}