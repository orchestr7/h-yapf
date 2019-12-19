# -*- coding: utf-8 -*-
"""
Function: all logic that is related with fixing style of docstring statements
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-12 18:11 Created
"""
import re

from yapf.yapflib.ordering_utils import move_lines_to_index, restore_lineno


class DocString:
    COPYRIGHT = re.compile('.*Copyright Information.*')
    FUNCTION = re.compile('.*Function:.*')
    CHANGE_HISTORY = re.compile('.*Change History:.*')

    def __init__(self, line, index_in_uwline):
        self.line = line
        self.token = line.first
        self.lines = [s.lstrip() for s in self.token.value.splitlines()]
        self.length = len(self.lines)
        self.index_in_uwline = index_in_uwline

    def check_regex(self, regex):
        for line in self.lines:
            if regex.match(line):
                return True
        return False

    def has_copyright(self):
        return self.check_regex(self.COPYRIGHT)

    def has_function_description(self):
        return self.check_regex(self.FUNCTION)

    def has_change_history(self):
        return self.check_regex(self.CHANGE_HISTORY)

    def set_copyright_pattern(self, match_pattern):
        self.COPYRIGHT = re.compile(match_pattern)


def get_copyright_doc_string(uwlines):
    uwline_index = 0
    for line in uwlines:
        # will check only first tokens as doc string cannot be anything else
        first_token = line.first

        # copyright doc string always should have no indents
        if first_token.is_docstring:
            return DocString(line, uwline_index)

        if not (first_token.is_comment or first_token.is_import_keyword):
            return None

        uwline_index += 1
    return None


def format_doc_string(uwlines, style):
    if style.Get('FORMAT_DOC_STRING'):
        doc_token = get_copyright_doc_string(uwlines)
        if doc_token:
            doc_token.token.value = '\n'.join(doc_token.lines)


def move_doc_string_to_head(uwlines, style):
    doc_string_pattern = style.Get(
        'AGGRESSIVELY_MOVE_DOC_STRING_TO_HEAD')
    if doc_string_pattern is not None:
        doc_token = get_copyright_doc_string(uwlines)

        # check that doc token exists and it is not the firstline
        if doc_token and doc_token.index_in_uwline != 0:
            doc_token.set_copyright_pattern(doc_string_pattern)

            # will move only global docstrings (with copyright)
            if doc_token.has_copyright():
                (move_to, lineno) = index_where_to_move_doc(uwlines)
                line_nums = move_lines_to_index(move_to, lineno, uwlines,
                                                [doc_token.line])
                restore_lineno(move_to, uwlines, line_nums, doc_token.length)


def index_where_to_move_doc(uwlines):
    for i, line in enumerate(uwlines):
        for token in uwlines[i].tokens:
            if not token.is_comment:
                return i, token.lineno
    return len(uwlines) - 1, uwlines[:-1].lineno
