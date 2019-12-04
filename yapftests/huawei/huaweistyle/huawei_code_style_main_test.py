# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of yapf application
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-11-26 18:23 Created
"""

import glob
import os
import sys

from yapftests import yapf_test_helper
from yapftests.huawei.huaweistyle.test_set import TestSet


class RunMainTest(yapf_test_helper.YAPFTest):
    INCORRECT = '_incorrect_'
    CORRECT = '_correct_'
    WARN = '_warning_'
    MSG_FILE = '.msg'
    RESOURCES_PATH = 'resources'

    def test(self):
        for test_name, test, expected in self.__get_test_sets():
            with self.subTest(msg=test_name):
                # test checks warnings (stderr)
                if self.WARN in test_name:
                    self.assertCodeEqual(expected, sys.stderr.get)

                # test checks fixes
                if self.INCORRECT in test_name:
                    self.assertCodeEqual(expected, test)

    def setUp(self):
        class RedirectedStdErr:
            get = ''

            def write(self, redirect_str):
                self.get = redirect_str

        self.__prev_state = sys.stderr
        sys.stderr = RedirectedStdErr()

    def tearDown(self):
        sys.stderr = self.__prev_state

    def __find_matching_resources(self, pattern):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            self.RESOURCES_PATH)
        return glob.glob(os.path.join(path, '*', f'*{pattern}.py'),
                         recursive=True)

    def __get_test_sets(self):
        """Create test sets for all test cases:
        1) that are expected to be fixed (_incorrect_)
        2) that are expected to generate a warning (_warning_)
         """
        test_set_res = TestSet()

        all_test_fixes = self.__find_matching_resources(self.INCORRECT)
        test_set_res.enrich(all_test_fixes, self.INCORRECT, self.CORRECT)

        all_test_warn = self.__find_matching_resources(self.WARN)
        test_set_res.enrich(all_test_warn, self.WARN + '.py', self.MSG_FILE)

        return sorted(test_set_res.test_set)
