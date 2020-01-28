# -*- coding: utf-8
"""
Function: Test for save_initial_idents_formatting option that controls if
 indents should be saved or not
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-03 18:03 Created
"""
import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup(self, value):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'save_initial_indents_formatting: {value}}}'))
        style.Set('JOIN_MULTIPLE_LINES', True)

    def test_on(self):
        self.__setup(True)
        self.assertTrue(style.Get('SAVE_INITIAL_INDENTS_FORMATTING'))

    def test_off(self):
        self.__setup(False)
        self.assertFalse(style.Get('SAVE_INITIAL_INDENTS_FORMATTING'))

    def test_save_indents(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
                        def fn():
                                if True:
                                 if True:
                                    if True:
                                                               print('True')
                        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_do_not_save_indentes(self):
        self.__setup(False)

        input_text = textwrap.dedent("""\
                        def fn():
                         # comment
                                if True:
                                 if True:
                                    if True:
                                                               print('True')
                        """)
        expected_text = textwrap.dedent("""\
                        def fn():
                            # comment
                            if True:
                                if True:
                                    if True:
                                        print('True')
                        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(expected_text, output_text)

    def test_online_stmt_wrapping(self):
        self.__setup(True)
        style.Set('JOIN_MULTIPLE_LINES', False)

        input_text = textwrap.dedent("""\
            if some_condition: pass
        """)
        expected_text = textwrap.dedent("""\
            if some_condition:
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(expected_text, output_text)

    def test_comments(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            def fn():
                      # comment 1
                      pass
                      # comment 2
                      pass
                      # comment 3
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_comments_after(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            def fn():
                      # comment 1
                      pass
                      # comment 2
                      pass
                      # comment 3
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)
