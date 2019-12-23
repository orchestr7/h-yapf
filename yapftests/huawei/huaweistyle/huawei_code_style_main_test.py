# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of yapf application
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-11-26 18:23 Created
"""

import contextlib
import glob
import os
import sys

from yapf.yapflib import yapf_api
from yapf.yapflib import style
from yapftests import yapf_test_helper

WINDOWS_EOL = '\r\n'
UNIX_EOL = '\n'


class RunMainTest(yapf_test_helper.YAPFTest):
    INCORRECT = '_incorrect_'
    CORRECT = '_correct_'
    WARN = '_warning_'
    MSG_FILE = '.msg'
    RESOURCES_PATH = 'resources'

    def test(self):
        for test_path, expected_path in self.__get_test_sets():
            test_name = os.path.basename(test_path)

            with self.subTest(msg=test_name):
                test = yapf_api.FormatFile(test_path)[0]
                test = test.replace(WINDOWS_EOL, UNIX_EOL)

                expected = self.__read_source(expected_path)

                # test checks warnings (stderr)
                if self.WARN in test_name:
                    self.assertCodeEqual(expected, sys.stderr.get)

                # test checks fixes
                if self.INCORRECT in test_name:
                    self.assertCodeEqual(expected, test)

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

        # resources' filenames do not fit any sound module naming rules
        # (it starts with a number), disable this option here
        #
        style.Set('CHECK_MODULE_NAMING_STYLE', False)

    @contextlib.contextmanager
    def subTest(self, msg, **params):
        self.setUpSubtest()
        with super().subTest(msg, **params):
            yield
        self.tearDownSubtest()

    def setUpSubtest(self):
        class RedirectedStdErr:
            def __init__(self):
                self.__messages = []

            @property
            def get(self):
                return ''.join(self.__messages)

            def write(self, redirect_str):
                self.__messages.append(redirect_str)

        self.__prev_state = sys.stderr
        sys.stderr = RedirectedStdErr()

    def tearDownSubtest(self):
        sys.stderr = self.__prev_state
        del self.__prev_state

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
        subtests = []

        subtests.extend(self.__find_tests(self.INCORRECT, self.CORRECT))
        subtests.extend(self.__find_tests(self.WARN, self.MSG_FILE,
                                          replace_suffix='.py'))

        return sorted(subtests)

    def __find_tests(self, test_pattern, expected_pattern, replace_suffix=''):
        test_paths = self.__find_matching_resources(test_pattern)

        def get_expected_path(test_path):
            return test_path.replace(f'{test_pattern}{replace_suffix}',
                                     expected_pattern)

        expected_paths = map(get_expected_path, test_paths)

        return zip(test_paths, expected_paths)

    def __read_source(self, path):
        # note that python 3 reads in "universal new line" mode by default,
        # i.e. any EOL markers ('\n', '\r', '\r\n') will be replaced with '\n'
        with open(path, 'r', encoding="utf-8") as file:
            return file.read()
