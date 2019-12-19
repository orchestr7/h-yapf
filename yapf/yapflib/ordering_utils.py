# -*- coding: utf-8 -*-
"""
Function: in this file you can find Utils related to ordering of source and
          changing the sequence of code lines
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-10 17:27 Created
"""
from yapf.yapflib import pytree_utils


def move_lines_to_index(uwline_index_to, lineno, uwlines, lines):
    """Method moves all lines in the list to the proper index of uwlines and
     update lineno on these lines. This is useful when you want to change the
     order of code lines. But note: it is not updating lineno on other lines

     @:returns positions (indexes) from original source where
      lines are taken from
    """
    # saving positions of imports here, that will be used for restoring 'lineno'
    lineno_where_line_was_taken_from = list()

    for line in lines:
        # FixMe PCS-23: optimize removing of line (remove -> filter?)
        uwlines.remove(line)
        lineno_where_line_was_taken_from.append(line.lineno)
        for token in line.tokens:
            token.node.lineno = lineno
            # hack to remove newlines between imports that we moved to top
            pytree_utils.SetNodeAnnotation(token.node,
                                           pytree_utils.Annotation.NEWLINES, 0)
            lineno += get_lineno_delta(token)
        # need to update lineno on import lines to have consistency
        lineno += 1

    uwlines[uwline_index_to:uwline_index_to] = lines
    return lineno_where_line_was_taken_from


def get_lineno_delta(token):
    return token.value.count('\n')


def restore_lineno(index_after_insert, uwlines,
                   lineno_where_lines_were_taken_from, shift_size):
    # do not restore lines for header + all imports that were inserted,
    # start changing lineno from index + import lines
    index_after_insert += len(lineno_where_lines_were_taken_from)

    for line in uwlines[index_after_insert:]:
        for tok in line.tokens:
            for num in lineno_where_lines_were_taken_from:
                if tok.lineno < num:
                    shift_token_down(tok, shift_size)

            # shifting all tokens after index to have newline after inserts
            shift_token_down(tok, 1)


def shift_token_down(tok, newlines_num):
    tok.node.lineno += newlines_num
