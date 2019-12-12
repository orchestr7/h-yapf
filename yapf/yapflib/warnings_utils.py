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

WARNINGS_DESCRIPTION = dict(
    ENCODING_WARNING=textwrap.dedent(
        "Each source file should have encoding header on the first or second line"
        " like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
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
    if style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        if len(uwlines) >= 1:
            first_line = uwlines[0]
            first_token = first_line.tokens[0]
            if first_token.is_comment:
                all_comments = first_token.value.split('\n')
                if is_encoding_in_first_or_second_line(all_comments):
                    return
            log_warn(WARNINGS_DESCRIPTION.get('ENCODING_WARNING'),
                     1, 1, os.path.basename(filename))


def is_encoding_in_first_or_second_line(comments):
    if len(comments) == 1:
        return bool(encoding_regex.match(comments[0]))
    if len(comments) == 2:
        return bool(encoding_regex.match(comments[0]) or
                encoding_regex.match(comments[1]))
    return False
