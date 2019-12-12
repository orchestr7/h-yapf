# -*- coding: utf-8 -*-
"""
Function: all logic that is related with warnins will be here
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 17:27 Created
"""
import os
import re
import sys
import textwrap

import threading

# Fixme : when we will make more warnings - we will need to split this file
from lib2to3.pgen2 import token

WARNINGS_DESCRIPTION = dict(
    ENCODING_WARNING=textwrap.dedent(
        "Each source file should have encoding header on the first or second "
        "line like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
    WILDCARD_IMPORT=textwrap.dedent(
        "Using of wildcard imports (import *) is a bad style in python, "
        "it makes code less readable and can cause potential code issues"
    )
)


def log_warn(warn_msg, line_number, column_num, filename):
    with threading.RLock():
        sys.stderr.write(f'WARN [filename: {filename}, '
                         f'line: {line_number}, '
                         f'column: {column_num}]: '
                         f'{warn_msg}\n')


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


# will check if header contains encoding declaration
# WARN: ENCODING_WARNING
# Control option: SHOULD_HAVE_ENCODING_HEADER
def check_encoding_in_header(uwlines, style, filename):
    if not style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        return

    if len(uwlines) >= 1:
        first_line = uwlines[0]
        first_token = first_line.tokens[0]
        if first_token.is_comment:
            all_comments = first_token.value.split('\n')
            if is_encoding_in_first_or_second_line(all_comments,
                                                   first_token.node.lineno):
                return
        log_warn(WARNINGS_DESCRIPTION.get('ENCODING_WARNING'),
                 1, 1, os.path.basename(filename))


def is_encoding_in_first_or_second_line(comments, lineno):
    # in case we have extra spaces in the beginning of the file -
    if lineno > len(comments):
        return False

    # comments - is a list of spitted comment-lines by '\n'
    if len(comments) >= 2:
        return (encoding_regex.match(comments[0]) or
                encoding_regex.match(comments[1]))

    if len(comments) == 1 and lineno == 1:
        return encoding_regex.match(comments[0])

    return False


# will wildcard imports should not be used in code
# WARN: WILDCARD_IMPORT
# Control option: SHOULD_HAVE_ENCODING_HEADER
def check_wildcard_imports(line, style, filename):
    if not style.Get('SHOULD_NOT_HAVE_WILDCARD_IMPORTS'):
        return

    for tok in line.tokens:
        next_token = tok.next_token
        if tok.is_import_keyword and next_token.node.type == token.STAR:
            log_warn(WARNINGS_DESCRIPTION.get('WILDCARD_IMPORT'),
                     tok.lineno, next_token.column, os.path.basename(filename))
            break


def check_all_recommendations(uwlines, style, filename):
    check_encoding_in_header(uwlines, style, filename)
    for line in uwlines:
        check_wildcard_imports(line, style, filename)
