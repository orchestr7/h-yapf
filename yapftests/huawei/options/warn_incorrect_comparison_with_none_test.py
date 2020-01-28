# -*- coding: utf-8
"""
Function: test WARN_INCORRECT_COMPARISON_WITH_NONE configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-18 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
import yapf.yapflib.warnings.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'warn_incorrect_comparison_with_none: {enable}}}'))

    def test_enabled(self):
        self.__setup(True)
        self.assertTrue(style.Get('WARN_INCORRECT_COMPARISON_WITH_NONE'))

    def test_disabled(self):
        self.__setup(False)
        self.assertFalse(style.Get('WARN_INCORRECT_COMPARISON_WITH_NONE'))

    def test_equal_to_none(self):
        self.__setup(True)

        input_source = textwrap.dedent("""\
            a == None
            b != None
            None == c
            None != d
        """)
        FormatCode(input_source)

        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'a is None')
        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'b is not None')
        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'c is None')
        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'd is not None')
        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 4)

    def test_complex_conditions(self):
        self.__setup(True)

        input_source = textwrap.dedent("""\
            a == b == None
            c == None and d == None
        """)
        FormatCode(input_source)

        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'b is None')
        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'c is None')
        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'd is None')
        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 3)

    def test_is_none(self):
        self.__setup(True)

        input_source = textwrap.dedent("""\
            a is None
            b is not None
        """)
        FormatCode(input_source)

        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 0)

    def test_compound_operands(self):
        self.__setup(True)

        input_source = textwrap.dedent("""\
            (a, b) == (None, None)
            [c, d] == (None, None)
        """)
        FormatCode(input_source)

        # ignore compond operands
        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 0)

    def test_func_call_operand(self):
        self.__setup(True)

        input_source = textwrap.dedent("""\
            fn(a) == None
        """)
        FormatCode(input_source)

        self.assertWarnMessage(warns.Warnings.COMP_WITH_NONE, 'fn\(a\) is None')
        self.assertWarnCount(warns.Warnings.COMP_WITH_NONE, 1)
