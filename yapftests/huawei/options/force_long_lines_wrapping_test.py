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

    def test_no_wrapping(self):
        self.__setup_import_splitter(True, column_limit=0)

        input_text = textwrap.dedent("""\
            variable = var1 + var2 * (var3 - var4)
        """)
        output_text = FormatCode(input_text)[0]

        expected_text = textwrap.dedent("""\
            variable = var1 + var2 * (var3 - var4)
        """)

        self.assertCodeEqual(expected_text, output_text)

    def test_enabled_lines(self):
        self.__setup_import_splitter(True, column_limit=30)

        input_text = textwrap.dedent("""\
            variable1 = var1 + var2 * (var3 - var4)
            variable2 = var1 + var2 * (var3 - var4)
        """)
        output_text = FormatCode(input_text, lines=[(2, 2)])[0]

        expected_text = textwrap.dedent("""\
            variable1 = var1 + var2 * (var3 - var4)
            variable2 = (var1 + var2 *
                         (var3 - var4))
        """)
        self.assertCodeEqual(expected_text, output_text)

    def test_preceding_comments(self):
        self.__setup_import_splitter(True, column_limit=20)

        # In this case the AST tree would look like in the tree below, and
        # we want it case to be properly handled (i.e. the comment should
        # be completely ignored):
        #
        #   if_stmt
        #     simple_stmt
        #       COMMENT '# ======...'
        #     NAME if
        #     atom
        #       LPAR (
        #       NAME some_value
        #       RPAR )
        #     ...
        #

        input_text = textwrap.dedent("""\
            # ==========================================
            if (some_value):
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)
