# -*- coding: utf-8
"""
Function: test INSERT_SPACE_AFTER_HASH_CHAR configuration paramenter
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-15 Created
"""

import textwrap

from yapf.yapflib import style, reformatter
from yapftests import yapf_test_helper


class RunMainTest(yapf_test_helper.YAPFTest):
    def __setup_import_splitter(self, enable):
        style.SetGlobalStyle(
            style.CreateStyleFromConfig(
                f'{{based_on_style: huawei, '
                f'insert_space_after_hash_char: {enable}}}'))

    def test_positive_case(self):
        self.__setup_import_splitter(True)
        self.assertTrue(style.Get('INSERT_SPACE_AFTER_HASH_CHAR'))

    def test_negative_case(self):
        self.__setup_import_splitter(False)
        self.assertFalse(style.Get('INSERT_SPACE_AFTER_HASH_CHAR'))
