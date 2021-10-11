import sys
import signal
from json import dumps
from flask import Flask, app, request
from flask_cors import CORS
import requests
from src.error import InputError
from src import config

# Implementation imports
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_join_v1, channel_details_v1

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

'''Example'''
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

'''Auth'''
@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():
    data = request.args
    resp = auth_register_v1(**data) # Already strings
    return resp

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    data = request.args
    resp = auth_login_v1(**data) # Already strings
    return resp

'''Channels'''
@APP.route('/channels/create/v2', methods=['POST'])
def channels_create():
    data = request.args
    # data['is_public'] is a string, comparing it to the string 'True' fixes this
    resp = channels_create_v1(data['token'], data['name'], data['is_public'] == 'True')
    return resp

'''Channel'''
@APP.route('/channel/join/v2', methods=['POST'])
def channel_join():
    data = request.args
    resp = channel_join_v1(data['token'], int(data['channel_id']))
    return resp

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details():
    data = request.args
    resp = channel_details_v1(data['token'], int(data['channel_id']))
    return resp

'''Clear'''
@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    resp = clear_v1()
    return resp

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
