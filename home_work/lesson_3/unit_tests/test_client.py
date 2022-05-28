import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from client import create_presence_message, process_server_message
import common.variables as constants


class TestClient(unittest.TestCase):
    test_message = {
        constants.ACTION: constants.PRESENCE,
        constants.TIME: 1.1,
        constants.USER: {
            constants.ACCOUNT_NAME: 'Guest',
        }
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_presence_message(self):
        checked_message = create_presence_message()
        checked_message['time'] = 1.1
        self.assertEqual(checked_message, self.test_message)

    def test_create_presence_message_user(self):
        checked_message = create_presence_message('user')
        checked_message['time'] = 1.1
        self.test_message[constants.USER][constants.ACCOUNT_NAME] = 'user'
        self.assertEqual(checked_message, self.test_message)

    def test_user_in_presence_message_in_list(self):
        checked_message = create_presence_message()
        checked_user = checked_message[constants.USER][constants.ACCOUNT_NAME]
        username_list = ['Guest', 'guest', 'User', 'user']
        self.assertIn(checked_user, username_list)

    def test_response_200(self):
        test_message = {constants.RESPONSE: 200}
        checked_message = '200: OK'
        self.assertEqual(process_server_message(test_message), checked_message)

    def test_response_400(self):
        test_message = {
            constants.RESPONSE: 400,
            constants.ERROR: 'error',
        }
        checked_message = '400: error'
        self.assertEqual(process_server_message(test_message), checked_message)

    def test_response_error(self):
        test_message = {}
        self.assertRaises(ValueError, process_server_message, test_message)

    def test_response_402(self):
        test_message = {
            constants.RESPONSE: 402,
            constants.ERROR: 'error',
        }
        checked_message = '402: no account with this name'
        self.assertNotEqual(process_server_message(test_message), checked_message)


if __name__ == '__main__':
    unittest.main()