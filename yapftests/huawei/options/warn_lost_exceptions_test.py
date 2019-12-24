# -*- coding: utf-8
"""
Function: test WARN_LOST_EXCEPTIONS configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-24 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
import yapf.yapflib.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'warn_lost_exceptions: {enable}}}'))

    def test_enabled(self):
        self.__setup(True)
        self.assertTrue(style.Get('WARN_LOST_EXCEPTIONS'))

    def test_disabled(self):
        self.__setup(False)
        self.assertFalse(style.Get('WARN_LOST_EXCEPTIONS'))

    def test_return(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            try:
                pass
            finally:
                return
        """)
        FormatCode(input_text)

        self.assertWarnMessage(warns.Warnings.LOST_EXCEPTION, 'return.*exception')
        self.assertWarnCount(warns.Warnings.LOST_EXCEPTION, 1)

    def test_break(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            try:
                pass
            finally:
                break
        """)
        FormatCode(input_text)

        self.assertWarnMessage(warns.Warnings.LOST_EXCEPTION, 'break.*exception')
        self.assertWarnCount(warns.Warnings.LOST_EXCEPTION, 1)

    def test_nested_stmt(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            try:
                pass
            finally:
                for _ in range(10):
                    break
        """)
        FormatCode(input_text)

        self.assertWarnCount(warns.Warnings.LOST_EXCEPTION, 0)
