# -*- coding: utf-8
"""
Function: Test for save_initial_idents_formatting option that controls if
 indents should be saved or not
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 12:38 Created
"""

import textwrap

from yapf.yapflib import style, reformatter
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __check_test(self, pos_case, formatted_code):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"blank_lines_after_indented_blocks: "
                                        f"{pos_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        def f():
                            if True:
                                print("#1")
                            print("#2")
                        print("#3")
                        """)

        uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
        self.assertCodeEqual(formatted_code,
                             reformatter.Reformat(uwlines))

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        def f():
                            if True:
                                print("#1")
                                
                            print("#2")
                            
                            
                        print("#3")
                        """)
        self.__check_test('True', formatted_code)

    def test_negative_case(self):
        formatted_code = textwrap.dedent("""\
                        def f():
                            if True:
                                print("#1")
                            print("#2")
                            
                            
                        print("#3")
                        """)
        self.__check_test('False', formatted_code)
