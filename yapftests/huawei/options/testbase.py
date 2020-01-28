# -*- coding: utf-8 -*-
"""
Function: Provides base classes for huawei options' tests.
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-17 Created
"""

import sys
import re
import json
from yapftests import yapf_test_helper


class WarnTestBase(yapf_test_helper.YAPFTest):
    def setUp(self):
        class RedirectedStdErr:
            def __init__(self):
                self.messages = []

            @property
            def get(self):
                return ''.join(self.messages)

            def write(self, redirect_str):
                try:
                    self.messages.append(json.loads(redirect_str))
                except json.JSONDecodeError:
                   pass


        self.__orig_stderr = sys.stderr
        self._stderr = RedirectedStdErr()
        sys.stderr = self._stderr

    def tearDown(self):
        sys.stderr = self.__orig_stderr
        del self.__orig_stderr
        del self._stderr


    def __filter_warns(self, warnno):
        def check_warnno(warn):
            return warn['WARN'] == warnno.value

        return filter(check_warnno, self._stderr.messages)


    def assertWarnMessage(self, warnno, pattern, lineno=None):
        def check_msg(warn):
            if lineno is not None and lineno != warn['line']:
                return False
            return re.search(pattern, warn['message'])

        try:
            warns = self.__filter_warns(warnno)
            next(filter(check_msg, warns))
        except StopIteration:
            self.fail(f'No such message: warn={warnno} (warnno={warnno.value})'
                      f' patern="{pattern}"')


    def assertWarnCount(self, warnno, expected):
        warns = list(self.__filter_warns(warnno))
        n_warns = len(warns)
        if n_warns != expected:
            self.fail(f'The warnings number mismatch: {n_warns} (actual) vs'
                      f' {expected} (expected)')
