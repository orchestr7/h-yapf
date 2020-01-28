# -*- coding: utf-8 -*-
"""
Function: RunMainTest class. Testing of SHOULD_HAVE_ENCODING_HEADER option
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-04 09:40 Created
"""
import sys
import textwrap

from yapf.yapflib import style, reformatter
from yapf.yapflib.warnings import warnings_utils
from yapf.yapflib.yapf_api import FormatCode
from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):

    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'should_not_have_wildcard_imports: {enable}}}'))

        unformatted_code = textwrap.dedent("""\
                        #!/usr/bin/env python
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment                       
                        from module import *
                        """)
        FormatCode(unformatted_code)

    def test_positive_case(self):
        self.__setup(True)

        self.assertWarnCount(warnings_utils.Warnings.WILDCARD_IMPORT, 1)
        self.assertWarnMessage(warnings_utils.Warnings.WILDCARD_IMPORT, lineno=5, pattern=".*wildcard.*")


    def test_negative_case(self):
        self.__setup(False)
        unformatted_code = textwrap.dedent("""\
                        #!/usr/bin/env python
                        # -*- coding: utf-8 -*-
                        import some_module
                        # some comment                       
                        from module import *
                        """)
        self.assertWarnCount(warnings_utils.Warnings.WILDCARD_IMPORT, 0)


