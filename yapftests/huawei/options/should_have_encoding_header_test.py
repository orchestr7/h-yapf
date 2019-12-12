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


class RunMainTest(yapf_test_helper.YAPFTest):
    def setUp(self):
        class RedirectedStdErr:
            get = ''

            def write(self, redirect_str):
                self.get = redirect_str

        self.__prev_state = sys.stderr
        sys.stderr = RedirectedStdErr()

    def tearDown(self):
        sys.stderr = self.__prev_state

    def __check_test(self, positive_case, formatted_code, option):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(f"{{based_on_style: huawei "
                                        f"{option}: "
                                        f"{positive_case}}}"))
        unformatted_code = textwrap.dedent("""\
                        import some_module
                        # some comment                       
                        """)

        uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
        reformatter.Reformat(uwlines, 'test_file')

        self.assertCodeEqual(formatted_code, sys.stderr.get)

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
                        WARN [filename: test_file, line: 1, column: 1]: Each 
                        source file should have encoding header on the first 
                        or second line like [# -*- coding: <encoding format> 
                        -*-] (see also: pep-0263)
                        """).replace('\n', '') + '\n'
        self.__check_test('True', formatted_code, 'should_have_encoding_header')

    def test_negative_case(self):
        formatted_code = textwrap.dedent('')
        self.__check_test('False', formatted_code,
                          'should_have_encoding_header')
