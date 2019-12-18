# -*- coding: utf-8 -*-
"""
Function: all logic that is related with fixing style of docstring statements
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-12 18:11 Created
"""
import re


class DocString:
    COPYRIGHT = re.compile('Copyright Information: Huawei.*')
    FUNCTION = re.compile('Function:.*')
    CHANGE_HISTORY = re.compile('Change History:.*')

    def __init__(self, doc_string_token, uwline_index):
        self.token = doc_string_token
        self.lines = [s.lstrip() for s in doc_string_token.value.splitlines()]
        self.uwline_index = uwline_index

    def check_regex(self, regex):
        for line in self.lines:
            if regex.match(line):
                return True
        return False

    def has_copyright(self):
        self.check_regex(self.COPYRIGHT)

    def has_function_description(self):
        self.check_regex(self.FUNCTION)

    def has_change_history(self):
        self.check_regex(self.CHANGE_HISTORY)


def get_copyright_doc_string(uwlines):
    still_reading_comments = True
    uwline_index = 0
    for line in uwlines:
        first_token = line.first

        if still_reading_comments and first_token.is_docstring:
            return DocString(first_token, uwline_index)

        if not first_token.is_comment:
            still_reading_comments = False
            return None

        uwline_index +=1
    return None


def format_doc_string(uwlines, style):
    if True or style.Get('FORMAT_COPYRIGHT_DOC_STRING'):
        doc_token = get_copyright_doc_string(uwlines)
        if doc_token:
            doc_token.token.value = '\n'.join(doc_token.lines)
