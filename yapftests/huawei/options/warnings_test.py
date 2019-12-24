# -*- coding: utf-8
"""
Function: test the warning mechanics
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
import yapf.yapflib.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def test_warn_location(self):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'check_var_naming_style: snake_case, '
                f'column_limit: 30}}'))

        input_source = textwrap.dedent("""\
            if left > right or right > left: pass
            SomeVariable = 0

            def fn():
                ''' fn
                description
                '''
                pass

            OtherVar = fn()
        """)
        FormatCode(input_source)

        # one line added becaus the `if` statement was wrapped
        self.assertWarnMessage(warns.Warnings.VAR_NAMING_STYLE,
            'line: 3.*SomeVariable')

        # two more line added as the style requires two blank lines
        # around top-level functions
        self.assertWarnMessage(warns.Warnings.VAR_NAMING_STYLE,
            'line: 13.*OtherVar')
