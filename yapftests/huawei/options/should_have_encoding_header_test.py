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
                        import some_module
                        # some comment                       
                        """)

        uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
        reformatter.Reformat(uwlines, 'test_file')

        self.assertCodeEqual(formatted_code, sys.stderr.get)

    def test_positive_case(self):
        formatted_code = textwrap.dedent("""\
            WARN 1: [filename: test_file, line: 1]: Each source file 
            should have encoding header on the first or second line like [# -*- 
            coding: <encoding format> -*-] (see also: pep-0263)
             """).replace('\n', '') + '\n'

        self.__check_test('True', formatted_code, 'should_have_encoding_header')

    def test_negative_case(self):
        formatted_code = ''

        self.__check_test('False', formatted_code,
                          'should_have_encoding_header')
