# -*- coding: utf-8
"""
Function: test WARN_MISSING_COPYRIGHT configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2020-01-28 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
import yapf.yapflib.warnings.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, enabled, pattern):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'warn_missing_copyright: {enabled} '
                f'copyright_pattern: {pattern}}}'))

    def test_on(self):
        self.__setup(True, '')
        self.assertTrue(style.Get('WARN_MISSING_COPYRIGHT'))

    def test_off(self):
        self.__setup(False, '')
        self.assertFalse(style.Get('WARN_MISSING_COPYRIGHT'))

    def test_warn_missing_copyright(self):
        self.__setup(True, 'Copyright: Huawei')

        input_source = textwrap.dedent("""\
            '''docstring
            There is no copyright
            '''
        """)
        FormatCode(input_source)

        self.assertWarnCount(warns.Warnings.MISSING_COPYRIGHT, 1)

    def test_copyright_is_present(self):
        self.__setup(True, 'Copyright: Huawei')

        input_source = textwrap.dedent("""\
            '''docstring
            Copyright: Huawei
            '''
        """)
        FormatCode(input_source)

        self.assertWarnCount(warns.Warnings.MISSING_COPYRIGHT, 0)
