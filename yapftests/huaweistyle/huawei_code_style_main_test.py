import glob
import os
import unittest

from yapf.yapflib import yapf_api


class RunMainTest(unittest.TestCase):
    INCORRECT = '_incorrect_'
    CORRECT = '_correct_'
    RESOURCES_PATH = 'resources'

    def __find_corresponding_result(self, test_filename):
        """All test files should have prefix INCORRECT, all expected result files should have prefix CORRECT"""
        expected_file_path = test_filename.replace(self.INCORRECT, self.CORRECT)
        with open(expected_file_path, 'r') as file:
            expected_str = file.read()
        return expected_str

    def __get_tested_str(self):
        """Run through resource path and run yapf on __incorrect__ files that should be fixed"""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.RESOURCES_PATH)
        all_test_files = glob.glob(os.path.join(path, '**', '*' + self.INCORRECT + '.py'), recursive=True)
        test_set = set()

        for test in all_test_files:
            expected_str = self.__find_corresponding_result(test)
            test_name_str = os.path.basename(test)
            test_str = yapf_api.FormatFile(test)[0]

            test_set.add((test_name_str, test_str, expected_str))
        return sorted(test_set)

    def test_run(self):
        for test_name, test, expected in self.__get_tested_str():
            with self.subTest(msg=test_name):
                self.assertEqual(test, expected)
