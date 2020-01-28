# -*- coding: utf-8
"""
Function: test SAVE_INITIAL_BLANKLINES configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2020-01-10 Created
"""

import textwrap

from yapf.yapflib import style
from yapf.yapflib.yapf_api import FormatCode
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup(self, name):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'save_initial_blanklines: {name}}}'))

    def test_on(self):
        self.__setup(True)
        self.assertTrue(style.Get('SAVE_INITIAL_BLANKLINES'))

    def test_off(self):
        self.__setup(False)
        self.assertFalse(style.Get('SAVE_INITIAL_BLANKLINES'))

    def test_toplevel_defs(self):
        self.__setup(True)
        style.Set('BLANK_LINES_AROUND_TOP_LEVEL_DEFINITION', 2)

        input_text = textwrap.dedent("""\
            def foo():
                pass

            def bar():
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_nested_defs(self):
        self.__setup(True)
        style.Set('BLANK_LINE_BEFORE_NESTED_CLASS_OR_DEF', True)

        input_text = textwrap.dedent("""\
            class Foo:
                class Nested:
                    pass
                def method(self):
                    pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_class_docstrings(self):
        self.__setup(True)
        style.Set('BLANK_LINE_BEFORE_CLASS_DOCSTRING', True)

        input_text = textwrap.dedent("""\
            class Foo:
                ''' docstring.'''
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_module_docstring(self):
        self.__setup(True)
        style.Set('BLANK_LINE_BEFORE_MODULE_DOCSTRING', True)

        input_text = textwrap.dedent("""\
            # comment
            ''' docstring.'''
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_blocks(self):
        self.__setup(True)
        style.Set('BLANK_LINES_AFTER_INDENTED_BLOCKS', True)

        input_text = textwrap.dedent("""\
            if cond:
                pass
            x = 1
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_comments(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            # top-level 1
            # top-level 2

            # top-level 3

            # function
            def func():
                # nested 1
                pass

                # nested 2
                # nested 3
            # top-level 4
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_expressions(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            def func():
                a = 1


                c = 3
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_comments_after_blocks(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            if condition:
                pass
            # comment
            else:
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_continuation(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            value = default_value \\
                if other_value is None else other_value
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)


    def test_blankline_after_block(self):
        self.__setup(True)
        style.Set('BLANK_LINES_AFTER_INDENTED_BLOCKS', True)

        input_text = textwrap.dedent("""\
            if condition:
                pass
            else:
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)

    def test_blankline_after_docstring(self):
        self.__setup(True)

        input_text = textwrap.dedent("""\
            def fn():
                ''' docstring
                line 1
                line 2
                line 3
                '''
                pass
        """)
        output_text = FormatCode(input_text)[0]

        self.assertCodeEqual(input_text, output_text)
