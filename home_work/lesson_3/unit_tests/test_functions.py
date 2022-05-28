import json
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.utils import get_message, send_message
import common.variables as constants


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(constants.ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(constants.ENCODING)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        'action': 'presence',
        'time': 1111.1111,
        'user': {
            'account_name': 'user',
        }
    }
    test_dict_recv_ok = {constants.RESPONSE: 200}
    test_dict_recv_err = {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad Request',
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_send_message_true(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        print(test_socket.encoded_message)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_message_with_error(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertRaises(TypeError, send_message, test_socket, 'wrong_dict')

    def test_get_message_ok(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)

    def test_get_message_error(self):
        test_sock_error = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(test_sock_error), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
