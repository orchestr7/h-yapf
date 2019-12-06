# -*- coding: utf-8 -*-
"""
Function: all logic that is related with warnins will be here
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 17:27 Created
"""
from enum import Enum, unique
import os
import re
import sys
import textwrap

import threading

from lib2to3.pygram import python_symbols as syms

from . import pytree_utils


@unique
class Warnings(Enum):
    ENCODING = 1
    GLOBAL_VAR_COMMENT = 2


WARNINGS_DESCRIPTION = {
    Warnings.ENCODING: textwrap.dedent(
        "Each source file should have encoding header on the first or second line"
        " like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
    Warnings.GLOBAL_VAR_COMMENT: textwrap.dedent(
        "Detailed comments should be added to each global variable"
    ),
}


def log_warn(warn, line_number, column_num, filename):
    with threading.RLock():
        sys.stderr.write(f'WARN {warn.value}: [filename: {filename}, '
                         f'line: {line_number}, '
                         f'column: {column_num}]: '
                         f'{WARNINGS_DESCRIPTION[warn]}\n')


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


# will check if header contains encoding declaration in 1st or 2nd line
# WARN: ENCODING_WARNING
# Control option: SHOULD_HAVE_ENCODING_HEADER
def check_encoding_in_header(uwlines, style, filename):
    if style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        if len(uwlines) >= 1:
            first_line = uwlines[0]
            first_token = first_line.tokens[0]
            if first_token.is_comment:
                comments = first_token.value.split('\n')
                if is_encoding_in_first_or_second_line(comments):
                    return
            log_warn(Warnings.ENCODING, 1, 1, os.path.basename(filename))


EOL_LINUX = '\n'


def is_comment_with_encoding(comment):
    return encode_regex.match(comment)


def is_encoding_in_first_or_second_line(comments):
    if len(comments) == 1:
        return bool(encoding_regex.match(comments[0]))
    if len(comments) >= 2:
        return bool(encoding_regex.match(comments[0]) or
                encoding_regex.match(comments[1]))
    return False


def _is_global_var_definition(uwl):
    return (uwl.depth == 0
        and uwl.tokens
        and pytree_utils.NodeName(uwl.first.node.parent) == 'expr_stmt'
        and uwl.first.is_name
        and uwl.first.value.isupper()
    )


def _is_comment_line(uwl):
    """ Check if a line is a comment contaning soething else apart from
    shebang or encoding definition.
    """

    if not uwl.is_comment:
        return False

    start_lineno = uwl.lineno - uwl.first.value.count('\n')
    total_lines = uwl.lineno - start_lineno + 1

    if start_lineno == 1 and total_lines <= 2:
        # check if the comment is shebang, or encoding, or shebabg
        # followed by encoding

        lines = uwl.first.value.split('\n')
        if total_lines == 1:
            return not (lines[0].startswith('#!')
                or is_encoding_in_first_or_second_line(lines)
            )
        else:
            return not (lines[0].startswith('#!')
                and is_encoding_in_first_or_second_line(lines)
            )

    return True


def check_if_global_vars_commented(uwlines, style, filename):
    if not style.Get('WARN_NOT_COMMENTED_GLOBAL_VARS'):
        return


    prev = None
    for uwl in uwlines:
        if _is_global_var_definition(uwl) and not _is_comment_line(prev):
            log_warn(Warnings.GLOBAL_VAR_COMMENT,
                uwl.lineno, uwl.first.column, os.path.basename(filename))
        prev = uwl
def get_str_with_encoding(comments_str):
    return next(
        filter(is_comment_with_encoding, comments_str.split(EOL_LINUX)), None
    )
