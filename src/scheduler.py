import time
from src.data_store import data_store
from src.message import (
    message_send_v1,
    message_senddm_v1
)

def send_msg_scheduler():
    '''
    Scheduler function used in conjunction with message_send_v1 and message_send_dm_v1.

    Will constantly check the message queue in the data store and determine whether the
    time matches with the desired time the message is supposed to be sent.
    '''
    while True:
        store = data_store.get()
        msg_queue = store['msg_queue']
        if len(msg_queue) == 0:
            continue
        first_msg = msg_queue[0]
        if int(time.time()) >= int(first_msg['time_sent']):
            if first_msg['type'] == 'channels':
                message_send_v1(first_msg['token'], first_msg['channel_id'], first_msg['message'], message_id=first_msg['message_id'])
            else:
                message_senddm_v1(first_msg['token'], first_msg['dm_id'], first_msg['message'], message_id=first_msg['message_id'])

            msg_queue.pop(0)
            data_store.set(store)
