# -*- coding: utf-8
"""
Function: test FORCE_LONG_LINES_WRAPPING configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 Created
"""

import textwrap

from yapf.yapflib import style, reformatter
from yapf.yapflib.style import StyleConfigError
from yapf.yapflib.yapf_api import FormatCode
import yapf.yapflib.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, name):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'check_var_naming_style: {name}}}'))

    def test_pascal_case(self):
        self.__setup('PascalCase')
        self.assertEqual(style.Get('CHECK_VAR_NAMING_STYLE'), 'PASCALCASE')

    def test_camel_case(self):
        self.__setup('camelCase')
        self.assertEqual(style.Get('CHECK_VAR_NAMING_STYLE'), 'CAMELCASE')

    def test_snake_case(self):
        self.__setup('snake_case')
        self.assertEqual(style.Get('CHECK_VAR_NAMING_STYLE'), 'SNAKECASE')

    def test_unknown_name(self):
        with self.assertRaises(StyleConfigError):
            self.__setup('unknown_name')

    def test_var_naming(self):
        self.__setup('snake_case')

        input_source = textwrap.dedent("""\
            CONSTANT_VAR = 0
            PascalCaseVar = 1
            camelCaseVar = 2
            snake_case_var = 3
            __SpecialVar__ = 4
        """)
        FormatCode(input_source)

        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'PascalCaseVar')
        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'camelCaseVar')
        self.assertWanrCount(warns.Warnings.VAR_NAMING_STYLE, 2)

    def test_local_vars(self):
        self.__setup('snake_case')

        input_source = textwrap.dedent("""\
            def fn():
                CONSTANT_VAR = 0
                PascalCaseVar = 1
                camelCaseVar = 2
                snake_case_var = 4
        """)
        FormatCode(input_source)

        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'PascalCaseVar')
        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'camelCaseVar')
        self.assertWanrCount(warns.Warnings.VAR_NAMING_STYLE, 2)

    def test_func_args(self):
        self.__setup('snake_case')

        input_source = textwrap.dedent("""\
            def fn(first_arg, secondArg, ThirdArg):
                pass
        """)
        FormatCode(input_source)

        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'secondArg')
        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'ThirdArg')
        self.assertWanrCount(warns.Warnings.VAR_NAMING_STYLE, 2)

    def test_func_capital_argname(self):
        self.__setup('snake_case')

        input_source = textwrap.dedent("""\
            def fn(ARG):
                pass
        """)
        FormatCode(input_source)

        # `ARG` is treated here as if it was a constant definition
        self.assertWanrCount(warns.Warnings.VAR_NAMING_STYLE, 0)

    def test_class_fields(self):
        self.__setup('snake_case')

        input_source = textwrap.dedent("""\
            class Class:
                PascalCaseStatic = 0
                snake_case_static = 1

                def __init__(self):
                    self.camelCase = 2
                    self.snake_case = 3
        """)
        FormatCode(input_source)

        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'PascalCaseStatic')
        self.assertWanrMessage(warns.Warnings.VAR_NAMING_STYLE, 'camelCase')
        self.assertWanrCount(warns.Warnings.VAR_NAMING_STYLE, 2)
