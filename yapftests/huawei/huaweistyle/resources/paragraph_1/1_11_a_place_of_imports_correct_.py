"""
Function: RunMainTest class. Testing of yapf application
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2019
Change History: 2019-11-26 18:23 Created
"""

import a
# comment before
# -*- coding: utf-8 -*-
# comment after

import b

# !/usr/bin/env python
import c

import d  # some comment to import1

from e import x
import f
import h
import k
import l
import m

# comment for global constant
GLOBAL_CONSTANT = 'import'


class A:
    a = 'import'


# some comment to import2 that we will leave here as we don't know
# if it is really related o import statement


def b():
    from g import g
    print(' ')
