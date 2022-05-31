import socket
import json
import time
import sys

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR
import logger.client_logger
import logging

LOG = logging.getLogger('app.client')


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


def process_server_message(message):
    LOG.debug(f'Message instance {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'{message[RESPONSE]}: OK'
        return f'{message[RESPONSE]}: {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port <= 1024 or server_port > 65535:
            LOG.critical(f'Wrong port {server_port}. Should be in range (1023:65536)')
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('wrong port number')
        sys.exit(1)

    LOG.info(f'Started client on server {server_address} on {server_port} port.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence_message()
    send_message(transport, message_to_server)
    try:
        answer = process_server_message(get_message(transport))
        LOG.info(f'Response from server accepted {answer}')
    except (ValueError, json.JSONDecodeError):
        LOG.error('Failed to decode received JSON string')


if __name__ == '__main__':
    main()
