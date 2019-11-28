"""
Function: RunMainTest class. Testing of yapf application
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-11-26 18:23 Created
"""

import glob
import os
import unittest

from yapf.yapflib import yapf_api
from yapf.yapflib import style


class RunMainTest(unittest.TestCase):
    INCORRECT = '_incorrect_'
    CORRECT = '_correct_'
    RESOURCES_PATH = 'resources'
    WINDOWS_EOL = '\r\n'
    UNIX_EOL = '\n'

    def __find_corresponding_result(self, test_filename):
        """All test files should have prefix INCORRECT, all expected result
         files should have prefix CORRECT
         """
        expected_file_path = test_filename.replace(self.INCORRECT, self.CORRECT)
        with open(expected_file_path, 'r') as file:
            expected_str = file.read()
        # small hack to fix changing of EOL to WIN format
        return expected_str.replace(self.WINDOWS_EOL, self.UNIX_EOL)

    def __get_tested_str(self):
        """Run through resource path and run yapf on __incorrect__ files
         that should be fixed
         """
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            self.RESOURCES_PATH)
        all_test_files = glob.glob(
            os.path.join(path, '*', f'*{self.INCORRECT}.py'), recursive=True)
        test_set = set()

        for test in all_test_files:
            test_name_str = os.path.basename(test)
            expected_str = self.__find_corresponding_result(test)
            test_str = yapf_api.FormatFile(test)[0]
            test_str = test_str.replace(self.WINDOWS_EOL, self.UNIX_EOL)

            test_set.add((test_name_str, test_str, expected_str))

        return sorted(test_set)

    @classmethod
    def setUpClass(cls):
        # We could as well pass `style_config='huawei'` to `FormatFile()`
        # but configuring via `setUpClass()` is the way used in other tests
        # (such as "reformatter_facebook_test").
        # Besides, even if we did passed `style_config`, `FormatFile()`
        # would call the very same `style.SetGlobalStyle()` inside itself
        # anyway.
        #
        style.SetGlobalStyle(style.CreateHuaweiStyle())

    def test_run(self):
        self.__get_tested_str()
        for test_name, test, expected in self.__get_tested_str():
            with self.subTest(msg=test_name):
                self.assertEqual(test, expected)
