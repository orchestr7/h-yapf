# -*- coding: utf-8 -*-
"""
Function: Formatt coments with respect to Huawei Code Style
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-10 Created
"""

import re

from . import style


def format_comments(uwlines):
    """ Format comments (inplace) according to Huawei Code Style
    """
    if not style.Get('INSERT_SPACE_AFTER_HASH_CHAR'):
        return uwlines

    for uwl in uwlines:
        if uwl.disable:
            continue

        # leave shebang as it is
        if (uwl.lineno == 1
            and uwl.tokens
            and uwl.first.value.startswith('#!')):
            continue

        for tok in uwl.tokens:
            if tok.is_comment:
                tok.value = _format_comment(tok.value)

    return uwlines


def _format_comment(text):
    return re.sub(r'(^|\n)#([^\s])', r'\1# \2', text)
