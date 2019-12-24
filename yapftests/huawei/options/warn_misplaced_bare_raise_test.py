# -*- coding: utf-8
"""
Function: test WARN_MISPLACED_BARE_RAISE configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-18 Created
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
                f'warn_misplaced_bare_raise: {enable}}}'))

    def test_enabled(self):
        self.__setup(True)
        self.assertTrue(style.Get('WARN_MISPLACED_BARE_RAISE'))

    def test_disabled(self):
        self.__setup(False)
        self.assertFalse(style.Get('WARN_MISPLACED_BARE_RAISE'))

    def _test_empty_raise(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            if True:
                raise
        """)
        FormatCode(input_text)

        self.assertWarnCount(warns.Warnings.MISPLACED_BARE_RAISE, 1)

    def _test_non_empty_raise(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            if True:
                raise Exception()
        """)
        FormatCode(input_text)

        self.assertWarnCount(warns.Warnings.MISPLACED_BARE_RAISE, 0)


    def test_raise_from_except(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            try:
                pass
            except:
                raise
        """)
        FormatCode(input_text)

        self.assertWarnCount(warns.Warnings.MISPLACED_BARE_RAISE, 0)
