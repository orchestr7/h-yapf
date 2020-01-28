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
    def __check_test(self, enable, pattern, formatted_code):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: pep8 "
                        f"aggressively_move_copyright_to_head: {enable} "
                        f"copyright_pattern: {pattern}}}"))
        unformatted_code = textwrap.dedent("""\
                        # -*- coding: utf-8 -*-
                        import a1
                        \"\"\"
                        Function: all logic that is related with fixing style of docstring statements
                        Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
                        Change History: 2019-12-12 18:11 Created
                        \"\"\"

                        # comment to func
                        def f():
                            print('a')
                        """)

        self.assertCodeEqual(formatted_code,
                             FormatCode(unformatted_code)[0])

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        # -*- coding: utf-8 -*-
                        \"\"\"
                        Function: all logic that is related with fixing style of docstring statements
                        Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
                        Change History: 2019-12-12 18:11 Created
                        \"\"\"

                        import a1


                        # comment to func
                        def f():
                            print('a')
                        """)
        self.__check_test(True, 'Copyright Information', formatted_code)

    def test_negative_case(self):
        formatted_code = textwrap.dedent("""\
                        # -*- coding: utf-8 -*-
                        import a1
                        \"\"\"
                        Function: all logic that is related with fixing style of docstring statements
                        Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
                        Change History: 2019-12-12 18:11 Created
                        \"\"\"


                        # comment to func
                        def f():
                            print('a')
                        """)
        self.__check_test(False, '', formatted_code)
