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

from lib2to3 import pytree
from lib2to3.pgen2 import token

from . import pytree_utils
from .format_token import FormatToken


@unique
class Warnings(Enum):
    ENCODING = 1
    GLOBAL_VAR_COMMENT = 2
    WILDCARD_IMPORT = 3
    CLASS_NAMING_STYLE = 4
    FUNC_NAMING_STYLE = 5
    VAR_NAMING_STYLE = 6


WARNINGS_DESCRIPTION = {
    Warnings.CLASS_NAMING_STYLE: textwrap.dedent(
        "Invalid class name"),
    Warnings.ENCODING: textwrap.dedent(
        "Each source file should have encoding header on the first or second "
        "line like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
    Warnings.FUNC_NAMING_STYLE: textwrap.dedent(
        "Invalid function name"),
    Warnings.GLOBAL_VAR_COMMENT: textwrap.dedent(
        "Global variable {variable} has missing detailed comment for it"
    ),
    Warnings.VAR_NAMING_STYLE: textwrap.dedent(
        "Invalid variable name: {variable}"),
    Warnings.WILDCARD_IMPORT: textwrap.dedent(
        "Using of wildcard imports (import *) is a bad style in python, "
        "it makes code less readable and can cause potential code issues"
    )
}


def log_warn(warn, line_number, column_num, filename, **msg):
    sys.stderr.write(f'WARN {warn.value}: [filename: {filename}, '
                     f'line: {line_number}, '
                     f'column: {column_num}]: '
                     f'{WARNINGS_DESCRIPTION[warn]}\n'.format(**msg))


# Describes naming style rules, such as
#    PascalCase
#    camelCase
#    snake_case
#
NAMING_STYLE_REGEXPS = dict(
    classname = dict(
        PASCALCASE = re.compile(r'[A-Z_][a-zA-Z0-9]+$'),
        CAMELCASE = re.compile(r'[a-z_][a-zA-Z0-9]+$'),
        SNAKECASE = re.compile(r'[a-z_][a-z0-9_]+$'),
    ),
    funcname = dict(
        PASCALCASE = re.compile(r'((_{0,2}[A-Z][a-zA-Z0-9]+)|(__.*__))$'),
        CAMELCASE = re.compile(r'((_{0,2}[a-z][a-zA-Z0-9]+)|(__.*__))$'),
        SNAKECASE = re.compile(r'((_{0,2}[a-z][a-z0-9_]+)|(__.*__))$'),
    ),
    varname = dict(
        PASCALCASE = re.compile(r'((_{0,2}[A-Z][a-zA-Z0-9]*)|(__.*__))$'),
        CAMELCASE = re.compile(r'((_{0,2}[a-z][a-zA-Z0-9]*)|(__.*__))$'),
        SNAKECASE = re.compile(r'((_{0,2}[a-z][a-z0-9_]*)|(__.*__))$'),
    ),
)


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


def check_all_recommendations(uwlines, style, filename):
    # FixMe: will need to reduce the number of usages of this method when chosen
    # FixME: style does not need these warnings (affecting performance)
    check_first_lines(uwlines, style, filename)
    prev_line = None
    for line in uwlines:
        warn_wildcard_imports(line, style, filename)
        warn_if_global_vars_not_commented(line, prev_line, style, filename)
        warn_class_naming_style(line, prev_line, style, filename)
        warn_func_naming_style(line, prev_line, style, filename)
        warn_vars_naming_style(line, prev_line, style, filename)
        prev_line = line


def check_first_lines(uwlines, style, filename):
    if len(uwlines) >= 1:
        first_line = uwlines[0]
        first_token = first_line.tokens[0]

        warn_if_no_encoding(first_token, style, filename)


# wildcard imports should not be used in code
# WARN: WILDCARD_IMPORT
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_wildcard_imports(line, style, filename):
    if not style.Get('SHOULD_NOT_HAVE_WILDCARD_IMPORTS'):
        return

    for tok in line.tokens:
        next_token = tok.next_token
        if tok.is_import_keyword and next_token.node.type == token.STAR:
            log_warn(Warnings.WILDCARD_IMPORT,
                     tok.lineno, next_token.column, os.path.basename(filename))
            break


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


# will check if header contains encoding declaration in 1st or 2nd line
# WARN: ENCODING_WARNING
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_if_no_encoding(first_token, style, filename):
    if style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        if first_token.is_comment:
            all_comments = first_token.value.split('\n')
            if is_comment_with_encoding(all_comments, first_token.lineno):
                return

        log_warn(Warnings.ENCODING,
                 first_token.lineno, 1, os.path.basename(filename))


def empty_newlines_in_the_beginning(lineno, comments):
    return lineno > len(comments)


def is_comment_with_encoding(comments, lineno):
    if empty_newlines_in_the_beginning(lineno, comments):
        return False

    # comments - is a list of spitted comment-lines by '\n'
    if len(comments) >= 2:
        return bool(encoding_regex.match(comments[0]) or
                    encoding_regex.match(comments[1]))

    if len(comments) == 1 and lineno == 1:
        return bool(encoding_regex.match(comments[0]))

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
                        or is_comment_with_encoding(lines, uwl.lineno)
                        )
        else:
            return not (lines[0].startswith('#!')
                        and is_comment_with_encoding(lines, uwl.lineno)
                        )

    return True


def warn_if_global_vars_not_commented(uwl, prev, style, filename):
    if not style.Get('WARN_NOT_COMMENTED_GLOBAL_VARS'):
        return

    if (_is_global_var_definition(uwl)
        and (prev is None or not _is_comment_line(prev))):
        log_warn(Warnings.GLOBAL_VAR_COMMENT,
                 uwl.lineno, uwl.first.column, os.path.basename(filename),
                 variable=uwl.first.value)


def get_str_with_encoding(comments_str, lineno):
    return next(
        filter(is_comment_with_encoding, (comments_str.split('\n'), lineno)),
        None
    )


def warn_class_naming_style(line, prev_line, style, filename):
    """ Check if class names fit the naming rule."""

    naming_style_name = style.Get('CHECK_CLASS_NAMING_STYLE')
    if not naming_style_name:
        return

    def is_class_definition(uwl):
        return (uwl.tokens
                and uwl.first.is_keyword
                and uwl.first.value == 'class'
                )

    def get_classname(uwl):
        tok = next(filter(lambda t: t.name == 'NAME', uwl.tokens[1:]))
        return tok.value

    if is_class_definition(line):
        naming_style = NAMING_STYLE_REGEXPS['classname'][naming_style_name]

        classname = get_classname(line)
        if not naming_style.match(classname):
            log_warn(Warnings.CLASS_NAMING_STYLE,
                     line.lineno, line.first.column, os.path.basename(filename))


def _is_func_definition(uwl):
    return (uwl.tokens
            and uwl.first.is_keyword
            and uwl.first.value == 'def'
            )


def warn_func_naming_style(line, prev_line, style, filename):
    """ Check if function (member or not) names fit the naming rule."""

    naming_style_name = style.Get('CHECK_FUNC_NAMING_STYLE')
    if not naming_style_name:
        return

    def get_funcname(uwl):
        tok = next(filter(lambda t: t.name == 'NAME', uwl.tokens[1:]))
        return tok.value

    if _is_func_definition(line):
        naming_style = NAMING_STYLE_REGEXPS['funcname'][naming_style_name]

        funcname = get_funcname(line)
        if not naming_style.match(funcname):
            log_warn(Warnings.FUNC_NAMING_STYLE,
                     line.lineno, line.first.column, os.path.basename(filename))


def warn_vars_naming_style(line, prev_line, style, filename):
    """ Check whether varibales and function argumens fit the naming rule."""

    naming_style_name = style.Get('CHECK_VAR_NAMING_STYLE')
    if not naming_style_name:
        return

    def is_expr(uwl):
        if not uwl.tokens:
            return

        node = uwl.first.node
        while node is not None:
            if (isinstance(node, pytree.Node)
                and pytree_utils.NodeName(node) == 'expr_stmt'):
                return True
            node = node.parent

        return False

    def is_assignment(uwl):
        return (is_expr(uwl)
                and next(filter(lambda t: t.is_name, uwl.tokens), None))

    def get_lhs_tokens(uwl):
        for tok in uwl.tokens:
            if tok.name == 'NAME':
                yield tok
            elif tok.name == 'EQUAL':
                break

    def iter_token_range(first, last):
        while True:
            yield first
            if first is last:
                break
            first = first.next_token

    def iter_parameters(paramlist):
        for item in paramlist:
            tokens = iter_token_range(item.first_token, item.last_token)
            tokens = filter(lambda t: t.name == 'NAME', tokens)
            first = next(tokens, None)
            assert first is not None
            yield first

    def get_func_args(uwl):
        for tok in uwl.tokens:
            if not tok.parameters:
                continue
            yield from iter_parameters(tok.parameters)

    if is_assignment(line):
        tokens = get_lhs_tokens(line)
    elif _is_func_definition(line):
        tokens = get_func_args(line)
    else:
        return

    naming_style = NAMING_STYLE_REGEXPS['varname'][naming_style_name]
    for tok in tokens:
        varname = tok.value

        # explicitly allow UPPER CASE names, because constants sould be
        # named this way regargless the naming style
        if not (varname == 'self'
                or varname.isupper()
                or naming_style.match(varname)):
            log_warn(Warnings.VAR_NAMING_STYLE,
                     tok.lineno, tok.column, os.path.basename(filename),
                     variable=tok.value)
