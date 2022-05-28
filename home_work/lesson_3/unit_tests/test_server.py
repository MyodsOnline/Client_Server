import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from server import process_client_message
import common.variables as constants


class TestServer(unittest.TestCase):
    err_dict = {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad request',
    }
    ok_dict = {
        constants.RESPONSE: 200,
    }
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

    def test_ok_check(self):
        self.assertEqual(process_client_message(self.test_message), self.ok_dict)

    def test_wrong_action(self):
        self.test_message[constants.ACTION] = 'wrong'
        self.assertEqual(process_client_message(self.test_message), self.err_dict)

    def test_no_action(self):
        del self.test_message[constants.ACTION]
        self.assertEqual(process_client_message(self.test_message), self.err_dict)

    def test_wrong_user(self):
        admin_list = ['Admin', 'admin']
        test_user = self.test_message[constants.USER][constants.ACCOUNT_NAME]
        self.assertNotIn(test_user, admin_list)

    def test_no_time(self):
        del self.test_message[constants.TIME]
        self.assertNotEqual(process_client_message(self.test_message), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
