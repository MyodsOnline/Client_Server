import socket
import json
import sys
import logging

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, USERNAME_DB
import logger.server_logger
from decos import log

SERVER_LOGGER = logging.getLogger('app.server')


@log
def process_client_message(message):
    SERVER_LOGGER.debug(f'Message instance from client: {message}')
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] in USERNAME_DB:
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            if listen_port <= 1024 or listen_port > 65535:
                raise ValueError
        else:
            listen_port = DEFAULT_PORT
    except IndexError:
        SERVER_LOGGER.critical(f'Missing port number')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Wrong port number')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except ValueError:
        SERVER_LOGGER.critical(f'missing IP address')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)
    print('waiting.........')

    while True:
        client_socket, client_address = transport.accept()
        SERVER_LOGGER.info(f'Connection with {client_address} established.')
        try:
            message_client = get_message(client_socket)
            SERVER_LOGGER.debug(f'Message "{message_client}" received.')
            server_response = process_client_message(message_client)
            SERVER_LOGGER.debug(f'Response to client: {server_response}')
            send_message(client_socket, server_response)
            SERVER_LOGGER.debug(f'Connection to client: {client_address} been closed.')
            client_socket.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error('some kind of error in the client message')
            client_socket.close()


if __name__ == '__main__':
    main()
