# -*- coding: utf-8
"""
Function: Test for AGGRESSIVELY_MOVE_ALL_IMPORTS_TO_HEAD option that reorder the
          sequence of source code
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-11 11:38 Created
"""

import textwrap

from yapf.yapflib import style, reformatter
from yapf.yapflib.yapf_api import FormatCode
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __check_test(self, pos_case, formatted_code):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"aggressively_move_all_imports_to"
                                        f"_head: "
                                        f"{pos_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        '''docs'''
                        # comment to import
                        import a1
                        
                        import a2  # want to have separated imports here
                        
                        # comment to func
                        def f():
                            import b
                        import c
                        """)

        self.assertCodeEqual(formatted_code,
                             FormatCode(unformatted_code)[0])

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        '''docs'''
                        # comment to import
                        import a1
                        
                        import a2  # want to have separated imports here
                        
                        import c


                        # comment to func
                        def f():
                            import b
                        """)
        self.__check_test('True', formatted_code)

    def test_negative_case(self):
        formatted_code = textwrap.dedent("""\
                        '''docs'''
                        # comment to import
                        import a1
                        
                        import a2  # want to have separated imports here
                        
                        
                        # comment to func
                        def f():
                            import b
                            
                            
                        import c
                        """)
        self.__check_test('False', formatted_code)
