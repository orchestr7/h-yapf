# -*- coding: utf-8
"""
Function: test FORCE_LONG_LINES_WRAPPING configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 Created
"""

import textwrap

from yapf.yapflib import style, reformatter
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup_import_splitter(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: huawei, '
                f'warn_not_commented_global_vars: {enable}}}'))

    def test_positive_case(self):
        self.__setup_import_splitter(True)
        self.assertTrue(style.Get('WARN_NOT_COMMENTED_GLOBAL_VARS'))

    def test_negative_case(self):
        self.__setup_import_splitter(False)
        self.assertFalse(style.Get('WARN_NOT_COMMENTED_GLOBAL_VARS'))
