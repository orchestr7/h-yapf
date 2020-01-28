# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of SHOULD_HAVE_ENCODING_HEADER option
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-04 09:40 Created
"""
import textwrap

from yapf.yapflib import style
from yapf.yapflib.warnings import warnings_utils
from yapf.yapflib.yapf_api import FormatCode
from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'should_have_encoding_header: {enable}}}'))
        input_source = textwrap.dedent("""\
                   def foo():
                       pass
                """)
        FormatCode(input_source)

    def test_positive_case(self):
        self.__setup(True)
        self.assertWarnMessage(warnings_utils.Warnings.ENCODING, lineno=1,
                               pattern='s')
        self.assertWarnCount(warnings_utils.Warnings.ENCODING, 1)

    def test_negative_case(self):
        self.__setup(False)
        self.assertWarnCount(warnings_utils.Warnings.ENCODING, 0)
