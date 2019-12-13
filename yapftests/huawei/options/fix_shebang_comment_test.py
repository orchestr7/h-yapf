# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of SHOULD_HAVE_ENCODING_HEADER option
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-13 15:40 Created
"""
import sys
import textwrap

from yapf.yapflib import style, reformatter
from yapf.yapflib.yapf_api import FormatCode
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __check_test(self, positive_case, formatted_code, option):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"{option}: "
                                        f"{positive_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        #!/usr/bin/python3 someopt
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment                       
                        """)

        self.assertCodeEqual(formatted_code,
                             FormatCode(unformatted_code)[0])

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        #!/usr/bin/env python3 someopt
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment
             """)

        self.__check_test('True', formatted_code, 'fix_shebang_header')

    def test_negative_case(self):
        formatted_code = textwrap.dedent("""\
                        #!/usr/bin/python3 someopt
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment
             """)

        self.__check_test('False', formatted_code, 'fix_shebang_header')
