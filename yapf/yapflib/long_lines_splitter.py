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
from . import pytree_utils
from . import style


def SplitLongLines(tree, enabled_lines):
  if style.Get('FORCE_LONG_LINES_WRAPPING'):
      splitter = _LongLinesSplitter(enabled_lines)
      splitter.Visit(tree)


class _LongLinesSplitter(pytree_visitor.PyTreeVisitor):
    """ Encolose long lines in parentheses, so that they can be correctly
    wrapped at later steps with respect to COLUMN_LIMIT.
    """

    def __init__(self, enabled_lines):
        super().__init__()
        self.enabled_lines = enabled_lines

       
    def Visit_if_stmt(self, node):
        for child in node.children:
            self.Visit(child)

        if self._condition_should_be_wrapped(node):
            self._insert_parens_between(node, 'if', ':')


    def Visit_while_stmt(self, node):
        for child in node.children:
            self.Visit(child)

        if self._condition_should_be_wrapped(node):
            self._insert_parens_between(node, 'while', ':')


    def Visit_arith_expr(self, node):
        def child_idx(child):
            for i, ch in enumerate(child.parent.children):
                if child is ch:
                    return i

        if self._arith_expr_should_be_wrapped(node):
            self_idx = child_idx(node)
            self._insert_parens(node.parent, self_idx, self_idx)


    def _line_should_be_wrapped(self, node):
        """ Return True if a line is longer than COLUMN_LIMIT."""

        if self.enabled_lines and node.get_lineno() not in self.enabled_lines:
            return False

        column_limit = style.Get('COLUMN_LIMIT')
        return column_limit and self._get_line_length(node) > column_limit


    def _condition_should_be_wrapped(self, node):
        """ Return True if a condition expression is longer than
        COLUMN_LIMIT and not enclosed in parentheses.
        """

        def is_comment_node(node):
            return (isinstance(node, pytree.Node)
                    and pytree_utils.IsCommentStatement(node))

        def has_parens(node):
            children = filter(lambda c: not is_comment_node(c), node.children)
            children = list(children)

            assert children[0].value in {'if', 'while'}
            return (len(children) >= 2
                    and children[1].type == syms.atom
                    and children[2].type == token.COLON)


        # If a condition is enclosed in parentheses then childer will look
        # like following: [{token if}, {atom}, {lpar} ...]
        # In this case we need not add extra parentheses.
        #
        return (self._line_should_be_wrapped(node)
            and not has_parens(node)
        )


    def _arith_expr_should_be_wrapped(self, node):
        """ Return True if an arithmetic expression is longer than
        COLUMN_LIMIT and not enclosed in parentheses.
        """

        # If an arithmetic statement is already within parentheses,
        # then the sub-tree will look as follows:
        #   expr_stmt
        #     atom
        #        lpar
        #        arith_stmt
        #        rpar
        #
        # We should not add parentheses is this case.
        #
        return (self._line_should_be_wrapped(node)
            and node.parent.type == syms.expr_stmt
        )


    def _get_line_length(self, node):
        def traverse(node):
            for child in node.children:
                if isinstance(child, pytree.Leaf):
                    if pytree_utils.NodeName(child) == 'COMMENT':
                        continue
                    else:
                        yield child.column + len(child.value.rstrip())
                elif node.type == syms.suite:  # the beginning of code block
                    break
                else:
                    yield from traverse(child)

        assert isinstance(node, pytree.Node)
        return max(traverse(node))

    def _insert_parens_between(self, node, begin_tok, end_tok):
        """ Insert parentheses between given token names."""

        def iter_leaves(node):
            for i, child in enumerate(node.children):
                if isinstance(child, pytree.Leaf):
                    yield i, child

        first = next(i for i, ch in iter_leaves(node) if ch.value == begin_tok)
        last = next(i for i, ch in iter_leaves(node) if ch.value == end_tok)

        first += 1
        last -= 1
        assert first >= last

        self._insert_parens(node, first, last)

    def _insert_parens(self, node, first_idx, last_idx):
        """ Insert parentheses around children range [first_idx, last_idx]

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

        def get_column(node):
            if isinstance(node, pytree.Leaf):
                return node.column
            return get_column(node.children[0])

        first = node.children[first_idx]
        last = node.children[last_idx]

        lpar = pytree.Leaf(token.LPAR,
            '(', context=('', (first.get_lineno(), get_column(first) - 1)))
        rpar = pytree.Leaf(token.RPAR,
            ')', context=('', (last.get_lineno(), get_column(last))))

        new_node = pytree.Node(syms.atom, [lpar, rpar])
        children = node.children[first_idx: last_idx + 1]
        for child in children:
            child.remove()
            new_node.insert_child(1, child)

        node.insert_child(first_idx, new_node)
