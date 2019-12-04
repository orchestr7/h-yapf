# -*- coding: utf-8
"""
Function: Test for save_initial_idents_formatting option that controls if
 indents should be saved or not
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-03 18:03 Created
"""
import textwrap

from yapf.yapflib import style, reformatter
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __check_test(self, pos_case, formatted_code):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"save_initial_idents_formatting: "
                                        f"{pos_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        def f():
                                if True:
                                 if True:
                                    if True:
                                                               print('True')
                        """)

        uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
        self.assertCodeEqual(formatted_code,
                             reformatter.Reformat(uwlines, 'test_file'))

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        def f():
                                if True:
                                 if True:
                                    if True:
                                                               print('True')
                        """)
        self.__check_test('True', formatted_code)

    def test_negative_case(self):
        formatted_code = textwrap.dedent("""\
                        def f():
                            if True:
                                if True:
                                    if True:
                                        print('True')
                                """)
        self.__check_test('False', formatted_code)
