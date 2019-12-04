# -*- coding: utf-8 -*-
"""
Function: Support for Recomendaion 1.7 of the Huawei Coding Style
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-06 Created
"""

from lib2to3 import pytree
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as syms

from . import pytree_visitor
from . import style


def SplitLongLines(tree, disabled_lines):
  if style.Get('FORCE_LONG_LINES_WRAPPING'):
      splitter = _LongLinesSplitter(disabled_lines)
      splitter.Visit(tree)


class _LongLinesSplitter(pytree_visitor.PyTreeVisitor):
    """ Encolose long lines in parentheses, so that they can be correctly
    wrapped at later steps with respect to COLUMN_LIMIT.
    """

    def __init__(self, disabled_lines):
        super().__init__()
        self.disabled_lines = disabled_lines

       
    def Visit_if_stmt(self, node):
        for child in node.children:
            self.Visit(child)

        if self._line_should_be_wrapped(node):
            self._insert_parens(node, 'if', ':')


    def Visit_while_stmt(self, node):
        for child in node.children:
            self.Visit(child)

        if self._line_should_be_wrapped(node):
            self._insert_parens(node, 'while', ':')


    def _line_should_be_wrapped(self, node):
        """ Return True if the line is longer that COLUMN_LIMIT
        and not enclosed in parentheses.
        """

        if self.disabled_lines and node.get_lineno() in self.disabled_lines:
            return False

        return (self._get_line_length(node) > style.Get('COLUMN_LIMIT')
            and not node.children[1].type == syms.atom
        )


    def _get_line_length(self, node):
        def traverse(node):
            for child in node.children:
                if isinstance(child, pytree.Leaf):
                    yield child.column + len(child.value.rstrip())
                elif node.type == syms.suite:  # the beginning of code block
                    break
                else:
                    yield from traverse(child)

        assert isinstance(node, pytree.Node)
        return max(traverse(node))


    def _insert_parens(self, node, begin_tok, end_tok):
        """ Insert parentheses between `begin_tok` and `end_tok`.

        For example, this function will change `node` as follows:

            # input subtree
            #
            if_stmt
                "if"
                and_test
                    ...
                ":" prefix=""
                suite prefix=""
                    ...

            # output subtree
            #
            if_stmt
                "if"
                atom
                    "("
                    and_test
                        ...
                    ")"
                ":" prefix=""
                suite prefix=""
                    ...
        """

        assert isinstance(node, pytree.Node)

        def get_leaves(node):
            for i, child in enumerate(node.children):
                if isinstance(child, pytree.Leaf):
                    yield i, child

        first_idx, first = next(
            (i, ch) for i, ch in get_leaves(node) if ch.value == begin_tok)
        last_idx, last = next(
            (i, ch) for i, ch in get_leaves(node) if ch.value == end_tok)

        lpar = pytree.Leaf(token.LPAR,
            '(', context=('', (first.get_lineno(), first.column - 1)))
        rpar = pytree.Leaf(token.RPAR,
            ')', context=('', (last.get_lineno(), last.column)))

        new_node = pytree.Node(syms.atom, [lpar, rpar])
        children = node.children[first_idx + 1: last_idx]
        for child in children:
            child.remove()
            new_node.insert_child(1, child)

        node.insert_child(first_idx + 1, new_node)
