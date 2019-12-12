# -*- coding: utf-8 -*-
"""
Function: in this file you can find Utils related to ordering of source and
          changing the sequence of code lines
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-10 17:27 Created
"""
from yapf.yapflib import pytree_utils


def order_main_code_blocks(uwlines, style):
    if style.Get("AGGRESSIVELY_MOVE_ALL_IMPORTS_TO_HEAD"):
        # now_reading_header flag will indicate when we have read imports/docs
        # at the beginning of the file that we don't want to move it or change
        now_reading_header = True

        imports_list = list()
        # this index will be used to get index where to place imports
        index_to_insert_imports = 0
        # line number of a position where imports will be inserted to
        lineno_for_imports = 0
        # lineno of a previous line before the line_for_imports
        prev_lineno = 0

        for line in uwlines:
            line_has_import_or_comment = False
            for token in line.tokens:
                if (token.is_import_keyword or
                        token.is_comment_or_doc_string):
                    line_has_import_or_comment = True

                # if we have found import statements that are not indented
                # (not in functions or if statements) - add them to list
                if (token.is_import_keyword and line.depth == 0 and
                        not now_reading_header):
                    imports_list.append(line)
                    break

            if now_reading_header:
                # calculate the number of comments in the beginning of the file
                # to this index we will insert our found imports
                if line_has_import_or_comment:
                    index_to_insert_imports += 1
                    prev_lineno = line.lineno
                else:
                    now_reading_header = False
                    lineno_for_imports = line.lineno

        # in case we have some statement with comments:
        #     # comment
        #     foo():
        # we don't want to split them and insert imports between them
        if lineno_for_imports - prev_lineno == 1:
            index_to_insert_imports -= 1
            lineno_for_imports = prev_lineno

        # if there are imports to insert - then insert them to the right index
        if imports_list:
            # method that moves all imports to the top of a source file and
            # returns a list with numbers of lines where imports will be taken
            lineno_where_line_was_taken_from = move_all_imports_to_head(
                index_to_insert_imports, lineno_for_imports,
                uwlines,
                imports_list)

            # restoring lineno after we have changed the order of lines
            restore_lineno(index_to_insert_imports,
                           uwlines,
                           lineno_where_line_was_taken_from)


def move_all_imports_to_head(index, lineno_of_imports,
                             uwlines, all_imports_in_file):
    # saving positions of imports here, that will be used for restoring 'lineno'
    lineno_where_line_was_taken_from = list()

    for import_line in all_imports_in_file:
        uwlines.remove(import_line)
        # need to update lineno on import lines to have consistency
        lineno_of_imports += 1
        lineno_where_line_was_taken_from.append(import_line.lineno)
        for token in import_line.tokens:
            token.node.lineno = lineno_of_imports
            # hack to remove newlines between imports that we moved to top
            pytree_utils.SetNodeAnnotation(token.node,
                                           pytree_utils.Annotation.NEWLINES, 0)

    uwlines[index:index] = all_imports_in_file
    return lineno_where_line_was_taken_from


def restore_lineno(index_after_imports, uwlines, lineno_where_line_was_taken_from):
    # do not restore lines for header + all imports that were inserted,
    # start changing lineno from index + import lines
    index_after_imports += len(lineno_where_line_was_taken_from)

    for line in uwlines[index_after_imports:]:
        for tok in line.tokens:
            for num in lineno_where_line_was_taken_from:
                if tok.lineno < num:
                    shift_token_down(tok, 1)

            # shifting all tokens after index to have newlines after imports
            shift_token_down(tok, 2)

def shift_token_down(tok, newlines):
    tok.node.lineno += newlines
