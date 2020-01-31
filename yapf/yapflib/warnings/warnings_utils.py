# -*- coding: utf-8 -*-
"""
Function: all logic that is related with warnins will be here
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-02 17:27 Created
"""
import collections
from functools import partial
import os
import re

from lib2to3 import pytree
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as syms

from yapf.yapflib.warnings.naming_styles import REGEXPS
from yapf.yapflib.warnings.warn_msg import Messages, Warnings
from .. import pytree_utils, pytree_visitor

encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


def check_all_recommendations(uwlines, style, filename):
    # FixMe: will need to reduce the number of usages of this method when chosen
    # FixME: style does not need these warnings (affecting performance)

    messages = Messages(filename)
    if style.Get('DISABLE_ALL_WARNINGS'):
        return messages

    warn_redefinition = RedefenitionChecker()
    warn_not_properly_encapsulated = ScriptsCodeIncapsulationChecker()

    modname = os.path.splitext(os.path.basename(filename))[0]

    warn_module_naming_style(messages, modname, style)
    check_first_lines(messages, uwlines, style)
    warn_missing_copyright(messages, modname, uwlines, style)

    prev_line = None
    for line in uwlines:
        warn_wildcard_imports(messages, line, style)
        warn_if_global_vars_not_commented(messages, line, prev_line, style)
        warn_class_naming_style(messages, line, style)
        warn_func_naming_style(messages, line, style)
        warn_vars_naming_style(messages, line, style)
        warn_redefinition(messages, line, style)
        warn_incorrect_comparison_with_none(messages, line, style)
        warn_not_properly_encapsulated(line, prev_line, style)
        warn_bare_except_clauses(messages, line, style)
        warn_lost_exception(messages, line, style)
        warn_misplaced_bare_raise(messages, line, style)
        prev_line = line

    warn_not_properly_encapsulated.end(messages)

    return messages


def check_first_lines(messages, uwlines, style):
    if len(uwlines) >= 1:
        first_line = uwlines[0]


        warn_if_no_encoding(messages, first_line, style)


# wildcard imports should not be used in code
# WARN: WILDCARD_IMPORT
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_wildcard_imports(messages, line, style):
    if not style.Get('SHOULD_NOT_HAVE_WILDCARD_IMPORTS'):
        return

    for tok in line.tokens:
        next_token = tok.next_token
        if tok.is_import_keyword and next_token.node.type == token.STAR:
            messages.add(tok, line.AsCode(), Warnings.WILDCARD_IMPORT)
            break


encoding_regex = re.compile('^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


# will check if header contains encoding declaration in 1st or 2nd line
# WARN: ENCODING_WARNING
# Control option: SHOULD_HAVE_ENCODING_HEADER
def warn_if_no_encoding(messages, first_line, style):
    if style.Get('SHOULD_HAVE_ENCODING_HEADER'):
        first_token = first_line.tokens[0]
        if first_token.is_comment:
            all_comments = first_token.value.split('\n')
            if is_comment_with_encoding(all_comments, first_token.lineno):
                return

        messages.add(first_token, first_line.AsCode(), Warnings.ENCODING)


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
    """ Check if a line is a comment contaning something else apart from
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
        messages.add(uwl.first, uwl.AsCode(), Warnings.GLOBAL_VAR_COMMENT,
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
        naming_style = REGEXPS['classname'][naming_style_name]

        classname_tok = get_classname(line)
        if not naming_style.match(classname_tok.value):
            messages.add(classname_tok, line.AsCode(), Warnings.CLASS_NAMING_STYLE,
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
        naming_style = REGEXPS['funcname'][naming_style_name]

        funcname_tok = get_funcname(line)
        if not naming_style.match(funcname_tok.value):
            messages.add(funcname_tok, line.AsCode(), Warnings.FUNC_NAMING_STYLE,
                         funcname=funcname_tok.value)


def warn_module_naming_style(messages, modname, style):
    """ Check if module names fit the naming rule."""

    naming_style_name = style.Get('CHECK_MODULE_NAMING_STYLE')
    if not naming_style_name:
        return

    # special cases, do nothing
    if modname in {'<stdin>', '<unknown>'}:
        return

    naming_style = REGEXPS['modname'][naming_style_name]
    if not naming_style.match(modname):
        messages.add_to_file(Warnings.MODULE_NAMING_STYLE, modname=modname)


def _find_parent(node, root, types):
    while node is not root:
        if node.type in types:
            return node
        node = node.parent

    return None


class _FindLValues(pytree_visitor.PyTreeVisitor):
    def __init__(self, root):
        self.lvalues = dict()
        self._stack = []
        self._chain = []

        self.Visit(root)

    def Visit_expr_stmt(self, node):
        try:
            for child in node.children:
                super().Visit(child)
        except StopIteration:
            pass

    def Visit_power(self, node):
        self._stack.append('power')

        try:
            for child in node.children:
                super().Visit(child)

            self.lvalues[id(self._chain[-1])] = [n.value for n in self._chain]

        except StopIteration:
            pass

        self._chain = []
        self._stack.pop()

    def Visit_NAME(self, node):
        if self._stack:
            self._chain.append(node)
        else:
            self.lvalues[id(node)] = [node.value]

    def Visit_LPAR(self, node):
        if self._stack:
            # it is a function call, skip arguments
            raise StopIteration()

    def Visit_LSQB(self, node):
        self.Visit_LPAR(node)

    def DefaultLeafVisit(self, node):
        # any of '=', '+=', '-=', etc.
        if 'EQUAL' in pytree_utils.NodeName(node):
            raise StopIteration()


def warn_vars_naming_style(messages, line, style):
    """ Check whether varibales and function argumens fit the naming rule."""

    naming_style_name = style.Get('CHECK_VAR_NAMING_STYLE')
    if not naming_style_name:
        return

    def is_expr(uwl):
        return (uwl.tokens
                and _find_parent(uwl.first.node, None, [syms.expr_stmt]))

    def is_assignment(uwl):
        return (is_expr(uwl)
                and next(filter(lambda t: t.is_name, uwl.tokens), None))

    def get_lhs_tokens(uwl):
        root = _find_parent(uwl.first.node, None, [syms.expr_stmt])
        lvalues = _FindLValues(root).lvalues

        for tok in uwl.tokens:
            if tok.name == 'EQUAL':
                break

            if tok.is_name and id(tok.node) in lvalues:
                chain = lvalues[id(tok.node)]
                if (len(chain) == 1
                        or (len(chain) == 2 and chain[0] == 'self')):
                    yield tok

    def iter_token_range(first, last):
        while True:
            yield first
            if first is last:
                break
            first = first.next_token

    def iter_parameters(paramlist):
        for item in paramlist:
            tokens = iter_token_range(item.first_token, item.last_token)
            tokens = filter(lambda t: t.name in {'NAME', 'STAR'}, tokens)
            first = next(tokens, None)

            if first is None:
                # This is possible when a comment is added to a function
                # argument (in some cases, when there is a trailing comma):
                #
                #     def fn(arg1,
                #         arg2, #comment
                #         arg3,
                #         ):
                #         pass
                #
                assert item.first_token.name == 'COMMENT'
                continue
            if first.name == 'STAR':
                yield next(tokens, first)
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

    naming_style = REGEXPS['varname'][naming_style_name]
    for tok in tokens:
        # explicitly allow UPPER CASE names, because constants sould be
        # named this way regargless the naming style
        if not (tok.value == 'self'
                or tok.value.isupper()
                or naming_style.match(tok.value)):
            messages.add(tok, line.AsCode(), Warnings.VAR_NAMING_STYLE, variable=tok.value)


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
            messages.add_anchor(first)
            messages.add(name, line.AsCode(), Warnings.REDEFININED, name=name.value,
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
    """ Warn when a comaprison to none uses `==` operator."""

    if not style.Get('WARN_INCORRECT_COMPARISON_WITH_NONE'):
        return

    def to_string(node):
        if isinstance(node, pytree.Leaf):
            return node.value
        else:
            return ''.join(l.value for l in node.leaves())

    def find_comp_exprs(line):
        for tok in line.tokens:
            if tok.is_binary_op and tok.value in {'==', '!='}:
                left = tok.node.prev_sibling
                right = tok.node.next_sibling

                # Ignore any compound operands (e.g. tuples)
                # is this case both operands would be `pytree.Node`.
                # `None` is always a `pytree.Leaf`, but the second operand
                # may not be if, for excample, it is a function call.

                if (isinstance(left, pytree.Leaf)
                        or isinstance(right, pytree.Leaf)):
                    yield left, tok, right

    def add_warn(op, operand):
        if op.value == '==':
            messages.add(op, line.AsCode(), Warnings.COMP_WITH_NONE,
                         var=to_string(operand), op='is')
        elif op.value == '!=':
            messages.add(op, line.AsCode(), Warnings.COMP_WITH_NONE,
                         var=to_string(operand), op='is not')

    for left, op, right in find_comp_exprs(line):
        if isinstance(left, pytree.Leaf) and left.value == 'None':
            add_warn(op, right)
        if isinstance(right, pytree.Leaf) and right.value == 'None':
            add_warn(op, left)


class ScriptsCodeIncapsulationChecker:
    """ Check whether a script uses `__name__ == '__main__' test.
    Here we assume that this check should be done whenever a file
    contains shebang, i.e. is designed to be exectuted directly.
    """

    stmt = re.compile(
        r'if[\\\s(]+__name__[\s\\]*==[\s\\]*[\'"]__main__[\'"][\\\s)]*:')

    def __init__(self):
        self.can_be_executed = False
        self.checks_for_main = False

    def __call__(self, line, prev_line, style):
        if not style.Get('CHECK_SCRIPT_CODE_ENCAPSULATION'):
            return

        if prev_line is None:
            if (line.tokens
                    and line.is_comment
                    and line.first.value.startswith('#!')):
                self.can_be_executed = True

        elif not self.can_be_executed:
            return

        elif not self.checks_for_main:
            self.checks_for_main = self.__check_for_main(line)

    def __check_for_main(self, line):
        if line.tokens and line.first.is_keyword and line.first.value == 'if':
            return self.stmt.match(str(line)) is not None

        return False

    def end(self, messages):
        if self.can_be_executed and not self.checks_for_main:
            messages.add_to_file(Warnings.SCRIPT_CODE_ENCAPSULATION)


def warn_bare_except_clauses(messages, line, style):
    """ Check if code uses bare `except` clauses."""

    if not style.Get('WARN_BARE_EXCEPT_CLAUSES'):
        return

    def is_exception_handler(line):
        return (line.tokens
                and line.first.is_keyword
                and line.first.value == 'except'
                )

    def lack_exception_type(line):
        return not any(tok.is_name for tok in line.tokens)

    if is_exception_handler(line) and lack_exception_type(line):
        messages.add(line.first, line.AsCode(), Warnings.BARE_EXCEPT)


def _is_on_the_right_of(node, target):
    def get_child_index(node):
        for i, ch in enumerate(node.parent.children):
            if ch is node:
                return i

    def by_name():
        for ch in reversed(node.parent.children[:idx]):
            if ch.type == token.NAME:
                return ch.value == target
        return False

    def by_type():
        for ch in reversed(node.parent.children[:idx]):
            if ch.type == target:
                return True
        return False

    idx = get_child_index(node)
    if isinstance(target, str):
        return by_name()
    return by_type()


def warn_lost_exception(messages, line, style):
    """ Warn if a return / break statement is executed from within
    a finally block."""

    if not style.Get('WARN_LOST_EXCEPTIONS'):
        return

    if not (line.tokens and line.first.value in {'return', 'break'}):
        return

    # Currently we ignore return/break statements in any nested stuctures
    # for simplicity. The reason is that in some case these statements
    # might not lead outse the final block:
    #
    #    try:
    #        pass
    #    finally:
    #        while True:
    #            break
    #
    def is_in_finally_block(node):
        if node.parent is None:
            return False

        if node.type == syms.suite:
            return _is_on_the_right_of(node, 'finally')

        return is_in_finally_block(node.parent)

    if is_in_finally_block(line.first.node):
        messages.add(line.first, line.AsCode(), Warnings.LOST_EXCEPTION,
                     stmt=line.first.value)


def warn_misplaced_bare_raise(messages, line, style):
    """ Check if all `raise` statements that do not specify an exception
    are called in `except` clauses."""

    if not style.Get('WARN_MISPLACED_BARE_RAISE'):
        return

    if not (line.tokens and line.first.value == 'raise'):
        return

    def is_in_except_clause(node):
        if node.parent is None:
            return False

        if node.type == syms.suite and node.parent.type == syms.try_stmt:
            return (_is_on_the_right_of(node, 'except')
                    or _is_on_the_right_of(node, syms.except_clause)
                    )

        return is_in_except_clause(node.parent)

    if not is_in_except_clause(line.first.node) and len(line.tokens) == 1:
        messages.add(line.first, line.AsCode(), Warnings.MISPLACED_BARE_RAISE)


def warn_missing_copyright(messages, modname, uwlines, style):
    if not style.Get('WARN_MISSING_COPYRIGHT'):
        return

    pattern = style.Get('COPYRIGHT_PATTERN')
    if not pattern:
        return

    for line in uwlines:
        if line.is_comment:
            continue
        if not line.is_docstring:
            break
        if not re.search(pattern, line.first.value):
            messages.add_to_file(Warnings.MISSING_COPYRIGHT, modname=modname)
        break
