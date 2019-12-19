# -*- coding: utf-8 -*-
"""
Function: all logic that is related with warnins will be here
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 17:27 Created
"""
from enum import Enum, unique
import collections
from functools import partial
import os
import re
import sys
import textwrap

from lib2to3 import pytree
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as syms

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
    REDEFININED = 7
    COMP_WITH_NONE = 8


WARNINGS_DESCRIPTION = {
    Warnings.CLASS_NAMING_STYLE: textwrap.dedent(
        "Invalid class name: {classname}"),
    Warnings.COMP_WITH_NONE: textwrap.dedent(
        "Comparison to none should be `{var} {op} None`"),
    Warnings.ENCODING: textwrap.dedent(
        "Each source file should have encoding header on the first or second "
        "line like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
    Warnings.FUNC_NAMING_STYLE: textwrap.dedent(
        "Invalid function name: {funcname}"),
    Warnings.GLOBAL_VAR_COMMENT: textwrap.dedent(
        "Global variable {variable} has missing detailed comment for it"
    ),
    Warnings.REDEFININED: textwrap.dedent(
        "'{name}' already defined here: lineno={first}"
    ),
    Warnings.VAR_NAMING_STYLE: textwrap.dedent(
        "Invalid variable name: {variable}"),
    Warnings.WILDCARD_IMPORT: textwrap.dedent(
        "Using of wildcard imports (import *) is a bad style in python, "
        "it makes code less readable and can cause potential code issues"
    )
}


class Messages:
    def __init__(self, filename):
        self.filename = os.path.basename(filename)
        self.messages = collections.defaultdict(list)
        self.line_numbers = dict()

    def add(self, tok, warn, **kwargs):
        self.messages[id(tok)].append((warn, kwargs))

    def remember_location(self, tok):
        if tok not in self:
            self.messages[id(tok)] = []

    def __contains__(self, tok):
        return id(tok) in self.messages

    def set_location(self, tok, lineno):
        self.line_numbers[id(tok)] = lineno

    def show(self):
        def format_msg(lineno, warn, kwargs):
            return (f'WARN {warn.value}: '
                    f'[filename: {self.filename}, line: {lineno}]: '
                    f'{WARNINGS_DESCRIPTION[warn]}'.format(**kwargs))

        def handle_callbacks(kwargs):
            for key, value in args.items():
                if callable(value):
                    args[key] = value()

        tokens = sorted(self.line_numbers.items(), key=lambda item: item[1])
        for tok_id, lineno in tokens:
            for warn, args in self.messages[tok_id]:
                handle_callbacks(args)
                sys.stderr.write('%s\n' % format_msg(lineno, warn, args))

    def get_lineno(self, tok):
        return self.line_numbers[id(tok)]


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
    prev_line = None
    messages = Messages(filename)

    warn_redefinition = RedefenitionChecker()

    check_first_lines(messages, uwlines, style)

    for line in uwlines:
        warn_wildcard_imports(messages, line, style)
        warn_if_global_vars_not_commented(messages, line, prev_line, style)
        warn_class_naming_style(messages, line, style)
        warn_func_naming_style(messages, line, style)
        warn_vars_naming_style(messages, line, style)
        warn_redefinition(messages, line, style)
        warn_incorrect_comparison_with_none(messages, line, style)
        prev_line = line

    return messages


def check_first_lines(messages, uwlines, style):
    if len(uwlines) >= 1:
        first_line = uwlines[0]
        first_token = first_line.tokens[0]

        warn_if_no_encoding(messages, first_token, style)


# wildcard imports should not be used in code
# WARN: WILDCARD_IMPORT
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_wildcard_imports(messages, line, style):
    if not style.Get('SHOULD_NOT_HAVE_WILDCARD_IMPORTS'):
        return

    for tok in line.tokens:
        next_token = tok.next_token
        if tok.is_import_keyword and next_token.node.type == token.STAR:
            messages.add(tok, Warnings.WILDCARD_IMPORT)
            break


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


# will check if header contains encoding declaration in 1st or 2nd line
# WARN: ENCODING_WARNING
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_if_no_encoding(messages, first_token, style):
    if style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        if first_token.is_comment:
            all_comments = first_token.value.split('\n')
            if is_comment_with_encoding(all_comments, first_token.lineno):
                return

        messages.add(first_token, Warnings.ENCODING)


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


def warn_if_global_vars_not_commented(messages, uwl, prev, style):
    if not style.Get('WARN_NOT_COMMENTED_GLOBAL_VARS'):
        return

    if (_is_global_var_definition(uwl)
        and (prev is None or not _is_comment_line(prev))):
        messages.add(uwl.first, Warnings.GLOBAL_VAR_COMMENT,
                     variable=uwl.first.value)


def get_str_with_encoding(comments_str, lineno):
    return next(
        filter(is_comment_with_encoding, (comments_str.split('\n'), lineno)),
        None
    )


def warn_class_naming_style(messages, line, style):
    """ Check if class names fit the naming rule."""

    naming_style_name = style.Get('CHECK_CLASS_NAMING_STYLE')
    if not naming_style_name:
        return

    def get_classname(uwl):
        tok = next(filter(lambda t: t.name == 'NAME', uwl.tokens[1:]))
        return tok

    if line.tokens and line.is_class_definition:
        naming_style = NAMING_STYLE_REGEXPS['classname'][naming_style_name]

        classname_tok = get_classname(line)
        if not naming_style.match(classname_tok.value):
            messages.add(classname_tok, Warnings.CLASS_NAMING_STYLE,
                         classname=classname_tok.value)


def warn_func_naming_style(messages, line, style):
    """ Check if function (member or not) names fit the naming rule."""

    naming_style_name = style.Get('CHECK_FUNC_NAMING_STYLE')
    if not naming_style_name:
        return

    def get_funcname(uwl):
        tok = next(filter(lambda t: t.name == 'NAME', uwl.tokens[1:]))
        return tok

    if line.tokens and line.is_func_definition:
        naming_style = NAMING_STYLE_REGEXPS['funcname'][naming_style_name]

        funcname_tok = get_funcname(line)
        if not naming_style.match(funcname_tok. value):
            messages.add(funcname_tok, Warnings.FUNC_NAMING_STYLE,
                         funcname=funcname_tok.value)


def warn_vars_naming_style(messages, line, style):
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
    elif line.tokens and line.is_func_definition:
        tokens = get_func_args(line)
    else:
        return

    naming_style = NAMING_STYLE_REGEXPS['varname'][naming_style_name]
    for tok in tokens:
        # explicitly allow UPPER CASE names, because constants sould be
        # named this way regargless the naming style
        if not (tok.value == 'self'
                or tok.value.isupper()
                or naming_style.match(tok.value)):
            messages.add(tok, Warnings.VAR_NAMING_STYLE, variable=tok.value)


class RedefenitionChecker:
    """ Generate warnings when a class / function / method is redefined."""

    def __init__(self):
        self.__names = collections.defaultdict(set)
        self.__first_defs = dict()

    def __call__(self, messages, line, style):
        if not style.Get('WARN_REDEFINITION'):
            return

        if not (line.tokens
                and (line.is_func_definition or line.is_class_definition)):
            return

        scope = id(self.__get_parent_scope(line))
        name = self.__get_name(line)

        if name.value in self.__names[scope]:
            first = self.__first_defs[(scope, name.value)]
            messages.remember_location(first)
            messages.add(name, Warnings.REDEFININED, name=name.value,
                first=partial(messages.get_lineno, first))

        else:
            self.__first_defs[(scope, name.value)] = name

        self.__names[scope].add(name.value)

    def __get_parent_scope(self, line):
        """ Returns the root node for the line's scope.

        For instance, for `my_method()` in the example below it
        would return a reference to the parent 'classdef' node.

            classdef
                NAME class
                NAME MyClass
                COLON
                suite
                    ...
                    funcdef
                        NAME def
                        name my_method
            ...
        """

        def if_class_or_func_def(node):
            return node.type == syms.classdef or node.type == syms.funcdef

        node = line.first.node.parent
        assert if_class_or_func_def(node)

        node = node.parent
        while node.parent is not None:
            if if_class_or_func_def(node):
                return node
            node = node.parent

        return node

    def __get_name(self, line):
        return next(filter(lambda t: t.name == 'NAME', line.tokens[1:]))


def warn_incorrect_comparison_with_none(messages, line, style):
    if not style.Get('WARN_INCORRECT_COMPARISON_WITH_NONE'):
        return

    def find_comp_exprs(line):
        for tok in line.tokens:
            if tok.is_binary_op and tok.value in {'==', '!='}:
                left = tok.node.prev_sibling
                right = tok.node.next_sibling
                assert type(left) == type(right)

                # ignore any compound operands (e.g. tuples)
                if isinstance(left, pytree.Leaf):
                    yield left, tok, right

    def add_warn(op, operand):
        if op.value == '==':
            messages.add(op, Warnings.COMP_WITH_NONE,
                         var=operand.value, op='is')
        elif op.value == '!=':
            messages.add(op, Warnings.COMP_WITH_NONE,
                         var=operand.value, op='is not')

    for left, op, right in find_comp_exprs(line):
        if left.value == 'None':
            add_warn(op, right)
        if right.value == 'None':
            add_warn(op, left)
