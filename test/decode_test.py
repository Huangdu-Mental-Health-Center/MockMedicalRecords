import unittest

from utils.jwt_util import decode_raw_jwt_and_return_user_id_str

with open("./test/demo_jwt.txt", "r") as demo_jwt_file:
    temp = demo_jwt_file.readlines()
    demo_jwt = temp[0]
    demo_jwt_expected_result = temp[1]

class TestDecoder(unittest.TestCase):

    def test_decode_if_success(self):
        result = decode_raw_jwt_and_return_user_id_str(demo_jwt)
        print(f"decoded result: {result}")
        self.assertTrue(result == demo_jwt_expected_result)

    def test_decode_if_fail(self):
        result = decode_raw_jwt_and_return_user_id_str("gw34vq566")
        print(f"decoded result: {result}")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()