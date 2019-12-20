# -*- coding: utf-8
"""
Function: test FORCE_LONG_LINES_WRAPPING configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup_import_splitter(self, enable, column_limit=80):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'force_long_lines_wrapping: {enable}, '
                f'column_limit: {column_limit}}}'))

    def test_positive_case(self):
        self.__setup_import_splitter(True)
        self.assertTrue(style.Get('FORCE_LONG_LINES_WRAPPING'))

    def test_negative_case(self):
        self.__setup_import_splitter(False)
        self.assertFalse(style.Get('FORCE_LONG_LINES_WRAPPING'))

    def test_if_statement(self):
        self.__setup_import_splitter(True, column_limit=20)

        input_text = textwrap.dedent("""\
            if variale1 and variable2:
                pass
        """)
        output_text = FormatCode(input_text)[0]

        expected_text = textwrap.dedent("""\
            if (variale1 and
                    variable2):
                pass
        """)

        self.assertCodeEqual(expected_text, output_text)


    def test_while_statement(self):
        self.__setup_import_splitter(True, column_limit=22)

        input_text = textwrap.dedent("""\
            while variale1 and variable2:
                pass
        """)
        output_text = FormatCode(input_text)[0]

        expected_text = textwrap.dedent("""\
            while (variale1
                   and variable2):
                pass
        """)

        self.assertCodeEqual(expected_text, output_text)


    def test_arith_expr(self):
        self.__setup_import_splitter(True, column_limit=30)

        input_text = textwrap.dedent("""\
            variable = var1 + var2 * (var3 - var4)
        """)
        output_text = FormatCode(input_text)[0]

        expected_text = textwrap.dedent("""\
            variable = (var1 + var2 *
                        (var3 - var4))
        """)

        self.assertCodeEqual(expected_text, output_text)
