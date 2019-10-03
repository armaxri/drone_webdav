#!/bin/python3

'''
Python script to allow a simple access of WebDAV servers from a drone.io file.
'''

import os
import sys
import inspect
from webdav3.client import Client


WEBDAV_CON_SETTINGS = [
    'webdav_hostname',
    'webdav_login',
    'webdav_password',
    'webdav_token',
    'webdav_root',
    'webdav_cert_path',
    'webdav_key_path',
    'webdav_recv_speed',
    'webdav_send_speed',
    'webdav_verbose',
    'proxy_hostname',
    'proxy_login',
    'proxy_password'
]


def load_env_value(env_name):
    '''Load the requested environment variable. If it's not present it returns an empty string.'''
    try:
        value = os.environ[env_name]
        return value
    except KeyError:
        return ''


def load_drone_param(drone_param):
    '''Loads parameters, which are coming from the drone configuration file file.'''

    # drone.io creates environment variables based on the name of the parameters.
    # Each parameter will be on uppercase and will be leaded by a 'PLUGIN_'.
    return load_env_value(('plugin_' + drone_param).upper())


def load_commandline_param(param):
    '''Check if a parameter was set on the command line.
    This functionality is just for development purposes.'''

    for argument in sys.argv:
        if argument.startswith('--' + param) or argument.startswith(param):
            return argument.split('=')[1]
    return ''


def get_webdav_options():
    '''Create a dictionary for the WebDAV client, based on environment variables.'''

    options = {}

    for setting in WEBDAV_CON_SETTINGS:
        value = load_drone_param(setting)
        if value != '':
            options[setting] = value

    return options


def get_client():
    '''Sets up the client object.'''

    options = get_webdav_options()
    return Client(options)


def execute_all_matching_perform_webdav_functions(function_name, client):
    '''Execute all functions that are matching the function name.'''

    functions = [obj for name, obj in inspect.getmembers(sys.modules[__name__])
                 if (inspect.isfunction(obj) and
                     name.startswith('perform_webdav_' + function_name))]

    if len(functions) == 0:
        print('Error: No function found for operation <' + function_name + '>.')
        sys.exit(1)

    # There should only be one match, since we don't have multiple functions with the same name.
    functions[0](client)


def check_and_return_connection():
    '''Check if the connection is working.'''

    client = get_client()
    if not client.valid():
        print(os.environ)
        for elem in os.environ:
            print(str(elem) + ': ' + os.environ[elem])
        print('Error: Settings are not valid!')
        sys.exit(1)

    return client


def perform_webdav_delete(client):
    '''Checks if a deletion is suppose to be performed and executes it in case.'''

    to_delete = load_commandline_param('delete')
    if to_delete != '':
        print('Deleting object <' + to_delete + '> on remote.')
        client = get_client()
        client.clean(to_delete)


def perform_webdav_move(client):
    '''Checks if a move operation is suppose to be performed and executes it in case.'''

    source = load_commandline_param('src')
    destination = load_commandline_param('dst')

    if source != '' and destination != '':
        print('Move on remote object <' + source + '> to <' + destination + '>.')
        client.move(source, destination)


def perform_webdav_copy(client):
    '''Checks if a copy operation is suppose to be performed and executes it in case.'''

    source = load_commandline_param('src')
    destination = load_commandline_param('dst')

    if source != '' and destination != '':
        print('Copy on remote object <' + source + '> to <' + destination + '>.')
        client.copy(source, destination)


def perform_webdav_list(client):
    '''List all files in a directory.'''

    dir2list = load_commandline_param('list')
    if dir2list != '':
        print('List all files on remote directory <' + dir2list + '>.')
        for file in client.list(dir2list):
            print(file)


def perform_webdav_mkdir(client):
    '''List all files in a directory.'''

    dir2be_created = load_commandline_param('mkdir')
    if dir2be_created != '':
        print('Create remote directory <' + dir2be_created + '>.')
        client.mkdir(dir2be_created)


def perform_webdav_upload(client):
    '''Uploads a file or directory to the server.'''

    source = load_commandline_param('src')
    destination = load_commandline_param('dst')

    if source != '' and destination != '':
        print('Upload local object <' + source + '> to remote <' + destination + '>.')
        client.upload(local_path=source, remote_path=destination)


def perform_webdav_download(client):
    '''Download a file or directory from the server.'''

    source = load_commandline_param('src')
    destination = load_commandline_param('dst')

    if source != '' and destination != '':
        print('Download remote object <' + source + '> to local <' + destination + '>.')
        client.download(remote_path=source, local_path=destination)


def main():
    '''Main function to select all operations.'''

    client = check_and_return_connection()

    # Sorry, but I'm really lazy and also adding all the functions by hand screams for errors.
    # Also each step will get his own client instance. Since there were some weird behaviors
    # during my tests, I prefer a fresh instance, which is always up to date.
    execute_all_matching_perform_webdav_functions(load_commandline_param('operation'), client)


if __name__ == "__main__":
    main()
