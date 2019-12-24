# -*- coding: utf-8
"""
Function: test WARN_REDEFINITION configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-18 Created
"""

from yapf.yapflib import style
import yapf.yapflib.warnings_utils as warns

from yapftests.huawei.options import testbase


class RunMainTest(testbase.WarnTestBase):
    def __setup(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: pep8, '
                f'warn_bare_except_clauses: {enable}}}'))

    def test_enabled(self):
        self.__setup(True)
        self.assertTrue(style.Get('WARN_BARE_EXCEPT_CLAUSES'))

    def test_disabled(self):
        self.__setup(False)
        self.assertFalse(style.Get('WARN_BARE_EXCEPT_CLAUSES'))
