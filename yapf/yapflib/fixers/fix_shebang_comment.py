# -*- coding: utf-8 -*-
"""
Function: all logic that is related with warnins will be here
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-12-12 18:11 Created
"""
import re

usr_bin_shebang = re.compile('^#![ \t]*/usr/bin/env[ |\t]?python.*')
usr_shebang = re.compile('^#![ \t]*/usr/bin.*')


# shebang with #!/usr/bin/env python should be used in the header of source file
# Control option: FIX_SHEBANG_HEADER
def fix_shebang_comment_header(uwlines, style):
    if style.Get('FIX_SHEBANG_HEADER'):
        first_line = uwlines[0]
        first_token = first_line.tokens[0]

        comments = first_token.value.split('\n')
        if comments:
            if (usr_shebang.match(comments[0]) and
                    not usr_bin_shebang.match(comments[0])):
                comments[0] = ('#!/usr/bin/env ' +
                               comments[0].rsplit('/', 1)[1])

                first_token.value = '\n'.join(comments)