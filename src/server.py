import sys
import signal
from json import dumps
from flask import Flask, app, request
from flask_cors import CORS
import requests
from src.error import InputError
from src import config

# For data persistence
from src.backup import interval_backup
import threading
import pickle
from src.data_store import data_store

# Implementation imports
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.other import clear_v1
from src.channel import channel_join_v1, channel_details_v1, channel_invite_v1, channel_messages_v1
from src.message import message_edit_v1, message_send_v1, message_remove_v1, message_senddm_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS


########### Example ############

# @APP.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })


########### Auth ############

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():
    data = request.get_json()
    resp = auth_register_v1(**data)
    return dumps(resp)

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    data = request.get_json()
    resp = auth_login_v1(**data)
    return dumps(resp)

@APP.route('/auth/logout/v1', methods=['POST'])
def auth_logout():
    data = request.get_json()
    resp = auth_logout_v1(**data)
    return dumps(resp)


########### Channels ############

@APP.route('/channels/create/v2', methods=['POST'])
def channels_create():
    data = request.get_json()
    resp = channels_create_v1(**data)
    return dumps(resp)

@APP.route('/channels/listall/v2', methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    resp = channels_listall_v1(token)
    return dumps(resp)

@APP.route('/channels/list/v2', methods=['GET'])
def channels_list():
    token = request.args.get('token')
    resp = channels_list_v1(token)
    return dumps(resp)


########### Channel ############

@APP.route('/channel/join/v2', methods=['POST'])
def channel_join():
    data = request.get_json()
    resp = channel_join_v1(**data)
    return dumps(resp)

@APP.route('/channel/invite/v2', methods=['POST'])
def channel_invite():
    data = request.get_json()
    resp = channel_invite_v1(**data)
    return dumps(resp)

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    resp = channel_details_v1(token, channel_id)
    return dumps(resp)

@APP.route('/channel/messages/v2', methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    resp = channel_messages_v1(token, channel_id, start)
    return dumps(resp)

########### Message ############

@APP.route('/message/send/v1', methods=['POST'])
def message_send():
    data = request.get_json()
    resp = message_send_v1(**data)
    return dumps(resp)

@APP.route('/message/senddm/v1', methods=['POST'])
def message_send():
    data = request.get_json()
    resp = message_senddm_v1(**data)
    return dumps(resp)

@APP.route('/message/edit/v1', methods=['PUT'])
def message_edit():
    data = request.get_json()
    resp = message_edit_v1(**data)
    return dumps(resp)

@APP.route('/message/remove/v1', methods=['DELETE'])
def message_remove():
    data = request.get_json()
    resp = message_remove_v1(**data)
    return dumps(resp)

########### Clear ############

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    resp = clear_v1()
    return dumps(resp)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    # Load in saved data
    try:
        # If previous data exists, load it in to the data store
        data = pickle.load(open("data.p", "rb"))
        data_store.set(data)
    except:
        # Otherwise, do nothing
        pass

    # Start periodic backup
    threading.Thread(target=interval_backup, args=()).start()

    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
