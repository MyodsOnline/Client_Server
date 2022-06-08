from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import logging
import argparse
import select
import time

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, USERNAME_DB, \
    SENDER, MESSAGE, MESSAGE_TEXT, CONNECTION_TIMEOUT
import logger.server_logger
from decos import log

SERVER_LOGGER = logging.getLogger('app.server')


@log
def process_client_message(message, messages_list, client):
    SERVER_LOGGER.debug(f'Message instance from client: {message}')
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] in USERNAME_DB:
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message \
            and message[ACTION] == MESSAGE \
            and TIME in message \
            and MESSAGE_TEXT in MESSAGE:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message({
            RESPONSE: 400,
            ERROR: 'Bad request'
        })
        return


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Wrong port: {listen_port}. Only [1024:65535] available.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = arg_parser()
    clients = []
    messages = []

    # with socket(AF_INET, SOCK_STREAM) as sock:
    #     sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #     sock.bind((listen_address, listen_port))
    #     sock.listen(MAX_CONNECTIONS)
    #     sock.settimeout(CONNECTION_TIMEOUT)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((listen_address, listen_port))
    sock.settimeout(CONNECTION_TIMEOUT)
    sock.listen(MAX_CONNECTIONS)

    print(f'.....waiting connection from {listen_port}:{listen_address}')
    SERVER_LOGGER.info(f'Server for {listen_port}:{listen_address} is running')

    while True:
        try:
            client, client_address = sock.accept()
        except OSError as err:
            print('...incoming connections:', err.errno)
            pass
        else:
            SERVER_LOGGER.info(f'.....connection with {client_address} established.....')
            clients.append(client)

        resv_data_list = []
        send_data_list = []
        err_list = []

        if clients:
            try:
                resv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
            except OSError:
                pass
            except Exception as ex:
                SERVER_LOGGER.debug(f'.....error: {ex} in select.....')

        if resv_data_list:
            for client_with_message in resv_data_list:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'.....client {client_with_message.getpeername()} disconnected.....')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]

            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'.....client {waiting_client.getpeername()} disconnected.....')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
