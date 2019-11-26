import glob
import os
import unittest
import re

from yapf.yapflib import yapf_api


class RunMainTest(unittest.TestCase):
    TEST_PATTERN = re.compile(r'.*[0-9]+_[0-9]+_a_.*')

    def __get_filename(self):
        return 0

    def __find_corresponding_result(self, test_filename, all_test_files):
        base_filename = test_filename.replace('_a_', '_b_')
        if base_filename in all_test_files:
          return base_filename
        else:
          raise Exception('Not able to find ' + base_filename + ' in ' + '/resource directory')


    def test(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        all_test_files = [f for f in glob.glob(path + "**/*.py", recursive=True)]
        for test in all_test_files:
            self.__find_corresponding_result(test, all_test_files)
            if self.TEST_PATTERN.match(test):
                # FixMe: finish comparing tests
                yapf_api.FormatFile(test)[0]
