import socket
import json
import time
import sys

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR


def create_presence_message(account_name='Guest'):
    output_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return output_message


def process_server_message(message):
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
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('wrong port number')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence_message()
    send_message(transport, message_to_server)
    try:
        answer = process_server_message(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('an error message from the server')


if __name__ == '__main__':
    main()
