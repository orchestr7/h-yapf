# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of SHOULD_HAVE_ENCODING_HEADER option
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-04 09:40 Created
"""
import sys
import textwrap

from yapf.yapflib import style, reformatter
from yapftests import yapf_test_helper
from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __check_test(self, positive_case, formatted_code, option):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"{option}: "
                                        f"{positive_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        #!/usr/bin/env python
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment                       
                        from module import *
                        """)

        uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
        reformatter.Reformat(uwlines, 'test_file')

        self.assertCodeEqual(formatted_code, sys.stderr.get)

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        WARN 3: [filename: test_file, line: 5]: 
                        Using of wildcard imports (import *) is a bad style in 
                        python, it makes code less readable and can cause 
                        potential code issues""").replace('\n', '') + '\n'
        self.__check_test('True', formatted_code,
                          'should_not_have_wildcard_imports')

    def test_negative_case(self):
        formatted_code = textwrap.dedent('')
        self.__check_test('False', formatted_code,
                          'should_not_have_wildcard_imports')
