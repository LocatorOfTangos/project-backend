import time
from src.data_store import data_store
from src.message import (
    message_send_v1,
    message_senddm_v1
)

def send_msg_scheduler():
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
