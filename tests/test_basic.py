import os
import pathlib
import unittest
from ask_robot.utils.basic import is_today_file_exist


class TestBasic(unittest.TestCase):
    def setUp(self) -> None:
        p = pathlib.Path(__file__).resolve()
        data_path = os.path.join(p, 'data')

        self.data_path = data_path

    def test_is_today_file_exist(self):
        test_filename = 'test_file.txt'
        actual = is_today_file_exist(test_filename)
        excepted = True
        self.assertEqual(actual, excepted)


if __name__ == '__main__':
    unittest.main()
