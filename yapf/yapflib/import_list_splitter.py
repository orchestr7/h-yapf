# -*- coding: utf-8
"""
Function: Split import statements when multipe modules are imported.
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-11-28 Created


Split import lists into a list of imports
```
    # input
    import a, b

    # output
    import a
    imoprt b
```

Instead of modifying unwrapped lines we could also change the parsed tree
itself. The point is that, unlike most other rules, here we not just
reformat some lines but actualy add new independed statements (like in
the example above, where there are two `import` statemnts in the output
vs a singe input statement).
"""


import copy

from . import format_token
from . import style
from . import unwrapped_line


def is_import_stmt(uwl):
    if not uwl.tokens:
        return False
    first_token = uwl.tokens[0]
    return first_token.is_keyword and first_token.value == 'import'


def has_comma(uwl):
    return any(tok.value == ',' for tok in uwl.tokens)


def split_import_list(uwl):
    def append(tokens, token):
        if tokens:
            tokens[-1].next_token = token
            token.previous_token = tokens[-1]
            token.node.lineno = tokens[0].lineno
        if token.is_name:
            token.spaces_required_before = True
        tokens.append(token)

    tokens = []
    for token in uwl.tokens:
        if token.value == ',':
            token.value = ';'
            tokens.append(token)

            new_tok = copy.copy(uwl.tokens[0])
            new_tok.must_break_before = True
            append(tokens, new_tok)

        elif not token.is_continuation:
            append(tokens, token)

    uwl.tokens[:] = tokens
    return uwl.Split()


def split_import_lists(uwlines):
    if not style.Get('SPLIT_SINGLE_LINE_IMPORTS'):
        return uwlines

    out_uwlines = []
    for uwl in uwlines:
        if not uwl.disable and is_import_stmt(uwl) and has_comma(uwl):
            out_uwlines.extend(split_import_list(uwl))
        else:
            out_uwlines.append(uwl)
    return out_uwlines
