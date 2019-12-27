# -*- coding: utf-8
"""
Function: test DISABLE_ALL_WARNINGS configuration paramenter
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
                f'disable_all_warnings: {enable}}}'))

    def test_enabled(self):
        self.__setup(True)
        self.assertTrue(style.Get('DISABLE_ALL_WARNINGS'))

    def test_disabled(self):
        self.__setup(False)
        self.assertFalse(style.Get('DISABLE_ALL_WARNINGS'))

    def test_disable_all(self):
        self.__setup(True)
        style.Set('WARN_INCORRECT_COMPARISON_WITH_NONE', True)
        style.Set('WARN_MISPLACED_BARE_RAISE', True)

        input_source = textwrap.dedent("""\
            a == None
            raise
        """)
        FormatCode(input_source)

        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 0)
