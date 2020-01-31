# -*- coding: utf-8 -*-
"""
Function: regexps that will be used to check naming style
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2020
"""

# Describes naming style rules, such as
#    PascalCase
#    camelCase
#    snake_case
#
import re

REGEXPS = dict(
    classname=dict(
        PASCALCASE=re.compile(r'[A-Z_][a-zA-Z0-9]+$'),
        CAMELCASE=re.compile(r'[a-z_][a-zA-Z0-9]+$'),
        SNAKECASE=re.compile(r'[a-z_][a-z0-9_]+$'),
    ),
    funcname=dict(
        PASCALCASE=re.compile(r'((_{0,2}[A-Z][a-zA-Z0-9]+)|(__.*__))$'),
        CAMELCASE=re.compile(r'((_{0,2}[a-z][a-zA-Z0-9]+)|(__.*__))$'),
        SNAKECASE=re.compile(r'((_{0,2}[a-z][a-z0-9_]+)|(__.*__))$'),
    ),
    modname=dict(
        PASCALCASE=re.compile(r'[A-Z_][a-zA-Z0-9]+$'),
        CAMELCASE=re.compile(r'[a-z_][a-zA-Z0-9]+$'),
        SNAKECASE=re.compile(r'[a-z_][a-z0-9_]+$'),
    ),
    varname=dict(
        PASCALCASE=re.compile(r'((_{0,2}[A-Z][a-zA-Z0-9]*)|(__.*__)|([_*]))$'),
        CAMELCASE=re.compile(r'((_{0,2}[a-z][a-zA-Z0-9]*)|(__.*__)|([_*]))$'),
        SNAKECASE=re.compile(r'((_{0,2}[a-z][a-z0-9_]*)|(__.*__)|([_*]))$'),
    ),
)
