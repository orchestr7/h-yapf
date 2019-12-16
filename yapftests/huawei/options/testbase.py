# -*- coding: utf-8 -*-
"""
Function: Provides base classes for huawei options' tests.
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-17 Created
"""

import sys
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
                self.messages.append(redirect_str)

        self.__orig_stderr = sys.stderr
        self._stderr = RedirectedStdErr()
        sys.stderr = self._stderr

    def tearDown(self):
        sys.stderr = self.__orig_stderr
        del self.__orig_stderr
        del self._stderr
