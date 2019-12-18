# -*- coding: utf-8 -*-
"""
Function: Formatt coments with respect to Huawei Code Style
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-10 Created
"""

from .. import style


def format_comments(uwlines):
    """ Format comments (inplace) according to Huawei Code Style
    """
    if not style.Get('INSERT_SPACE_AFTER_HASH_CHAR'):
        return uwlines

    for uwl in uwlines:
        if uwl.disable:
            continue

        for tok in uwl.tokens:
            if tok.is_comment:
                tok.value = _format_comment(tok)

    return uwlines


def _format_comment(tok):
    lines = tok.value.split('\n')
    start_lineno = tok.lineno - len(lines) + 1

    for i in range(len(lines)):
        lineno = start_lineno + i
        if lineno == 1 and lines[i].startswith('#!'):
            continue
        if lines[i].strip() == '#':
            continue
        if not lines[i].startswith('# '):
            lines[i] = '# ' + lines[i][1:]

    return '\n'.join(lines)
