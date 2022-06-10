import socket
import json
import time
import sys
import logging
import argparse

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, SENDER, MESSAGE, MESSAGE_TEXT
import logger.client_logger
from decos import log

LOG = logging.getLogger('app.client')


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Received message from user {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOG.info(f'Received message from user {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOG.error(f'Received an invalid message from the server: {message}')


@log
def create_message(sock, account_name='Guest'):
    message = input('Input message or "!!!" to exit > ')
    if message == '!!!':
        sock.close()
        LOG.info('Ending by user command')
        print('Program is over')
        sys.exit(0)

    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOG.debug(f'Message Formed: {message_dict}')
    return message_dict


@log
def create_presence_message(account_name='Guest'):
    output_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOG.debug(f'Message "{PRESENCE}" for user: {account_name}')
    return output_message


@log
def process_server_message(message):
    LOG.debug(f'Message instance {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'{message[RESPONSE]}: OK'
        return f'{message[RESPONSE]}: {message[ERROR]}'
    raise ValueError


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        LOG.critical(
            f'...wrong port: {server_port}. Available values [1024:65535]')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        LOG.critical(f'Unacceptable operation mode is indicated: {client_mode}, Available values listen or send')
        sys.exit(1)

    return server_address, server_port, client_mode


@log
def main():
    server_address, server_port, client_mode = arg_parser()

    LOG.info(f'Started client on server {server_address}: {server_port} on {client_mode} mode.')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))
    except ConnectionRefusedError:
        LOG.critical(f'Failed to connect to server {server_port}:{server_address}')
        sys.exit(1)

    try:
        message_to_server = create_presence_message()
        send_message(sock, message_to_server)
        server_response = get_message(sock)
        print(process_server_message(server_response))
        LOG.info(f'Connection to the server is successful. Server response: {server_response}')
        print(f'Connection to the server is successful. Server response: {server_response}')
    except (ValueError, json.JSONDecodeError):
        LOG.error('Failed to decode received JSON string')

    else:
        if client_mode == 'send':
            print('Operation mode - sending messages')
        else:
            print('Operation mode - receiving messages')
        while True:
            if client_mode == 'send':
                try:
                    send_message(sock, create_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'The connection to server {server_address} has been lost.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'The connection to server {server_address} has been lost.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
