from src.data_store import data_store
import os
from shutil import rmtree

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
    store['dms'] = []
    store['passwords'] = []
    store['curr_channel_id'] = 0
    store['curr_session_id'] = 0
    store['message_info'] = {}
    store['workplace_stats'] = {}
    store['current_profile_img'] = 0
    data_store.set(store)

    images = 'profile_imgs'
    for filename in os.listdir(images):
        if filename == 'profile_img_default.jpg':
            continue
        file_path = os.path.join(images, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            raise 'Failed to delete %s. Reason: %s' % (file_path, e)

    return {}