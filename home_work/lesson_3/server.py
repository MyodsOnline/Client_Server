import socket
import json
import time
import sys

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, ENCODING, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, USERNAME_DB


def process_client_message(message):
    if ACTION in message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request from here'
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
        print('missing port number')
        sys.exit(1)
    except ValueError:
        print('wrong port number')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except ValueError:
        print('missing IP address')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client_socket, client_address = transport.accept()
        try:
            message_client = get_message(client_socket)
            print(message_client)
            server_response = process_client_message(message_client)
            send_message(client_socket, server_response)
            client_socket.close()
        except (ValueError, json.JSONDecodeError):
            print('some kind of error in the client message')
            client_socket.close()


if __name__ == '__main__':
    main()
