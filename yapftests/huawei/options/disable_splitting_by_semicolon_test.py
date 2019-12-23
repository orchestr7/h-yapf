# -*- coding: utf-8
"""
Function: test DISABLE_SPLITTING_BY_SEMICOLON configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 Created
"""

import textwrap

from yapf.yapflib import style
from yapftests import yapf_test_helper
from yapf.yapflib.yapf_api import FormatCode


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'disable_splitting_by_semicolon: {enable}}}'))

    def test_positive_case(self):
        self.__setup(True)
        self.assertTrue(style.Get('DISABLE_SPLITTING_BY_SEMICOLON'))

        formatted_text = FormatCode(textwrap.dedent("""\
            a = 1; b = 2
        """))[0]

        expected_text = textwrap.dedent("""\
            a = 1; b = 2
        """)

        self.assertCodeEqual(expected_text, formatted_text)

    def test_negative_case(self):
        self.__setup(False)
        self.assertFalse(style.Get('DISABLE_SPLITTING_BY_SEMICOLON'))

        formatted_text = FormatCode(textwrap.dedent("""\
            a = 1; b = 2
        """))[0]

        expected_text = textwrap.dedent("""\
            a = 1
            b = 2
        """)

        self.assertCodeEqual(expected_text, formatted_text)
