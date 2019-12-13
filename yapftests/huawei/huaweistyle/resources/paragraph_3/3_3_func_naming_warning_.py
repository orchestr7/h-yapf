# -*- coding: utf-8 -*-


def invalidTopLevel():
    def invalidInner():
        pass

    def valid_inner():
        pass


def valid_top_level():
    pass


class SomeClass:
    def __init__(self):
        pass

    def invalidPublic(self):
        pass

    def valid_public(self):
        pass

    def _invalidProtected(self):
        pass

    def _valid_protected(self):
        pass

    def __invalidPrivate(self):
        pass

    def __valid_private(self):
        pass
