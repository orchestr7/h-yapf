import json
import os
import sys
import textwrap
from enum import unique, Enum


@unique
class Warnings(Enum):
    ENCODING = 1
    GLOBAL_VAR_COMMENT = 2
    WILDCARD_IMPORT = 3
    CLASS_NAMING_STYLE = 4
    FUNC_NAMING_STYLE = 5
    VAR_NAMING_STYLE = 6
    REDEFININED = 7
    COMP_WITH_NONE = 8
    MODULE_NAMING_STYLE = 9
    SCRIPT_CODE_ENCAPSULATION = 10
    BARE_EXCEPT = 11
    LOST_EXCEPTION = 12
    MISPLACED_BARE_RAISE = 13
    MISSING_COPYRIGHT = 14
    AGGRESSIVELY_MOVE_COPYRIGHT_TO_HEAD = 15


WARNINGS_DESCRIPTION = {
    Warnings.BARE_EXCEPT: textwrap.dedent(
        "No exception type(s) specified."),
    Warnings.CLASS_NAMING_STYLE: textwrap.dedent(
        "Invalid class name: {classname}"),
    Warnings.COMP_WITH_NONE: textwrap.dedent(
        "Comparison to none should be `{var} {op} None`"),
    Warnings.ENCODING: textwrap.dedent(
        "Each source file should have encoding header on the first or second "
        "line like [# -*- coding: <encoding format> -*-] (see also: pep-0263)"),
    Warnings.FUNC_NAMING_STYLE: textwrap.dedent(
        "Invalid function name: {funcname}"),
    Warnings.GLOBAL_VAR_COMMENT: textwrap.dedent(
        "Global variable {variable} has missing detailed comment for it"
    ),
    Warnings.LOST_EXCEPTION: textwrap.dedent(
        "'{stmt}' in finally block may swallow exception"),
    Warnings.MISPLACED_BARE_RAISE: textwrap.dedent(
        "The raise statement is not inside an except clause"),
    Warnings.MISSING_COPYRIGHT: textwrap.dedent(
        "The copyright in missing in {modname}"),
    Warnings.MODULE_NAMING_STYLE: textwrap.dedent(
        "Invalid module name: {modname}"),
    Warnings.REDEFININED: textwrap.dedent(
        "'{name}' already defined here: lineno={first}"
    ),
    Warnings.SCRIPT_CODE_ENCAPSULATION: textwrap.dedent(
        "All top-level code should be encapsulated in functions or classes. "
        "Wrap it into `if __name__ == '__main__'` block."
    ),
    Warnings.VAR_NAMING_STYLE: textwrap.dedent(
        "Invalid variable name: {variable}"),
    Warnings.WILDCARD_IMPORT: textwrap.dedent(
        "Using of wildcard imports (import *) is a bad style in python, "
        "it makes code less readable and can cause potential code issues"
    ),
    Warnings.AGGRESSIVELY_MOVE_COPYRIGHT_TO_HEAD: textwrap.dedent(
      "Module comments (with copyright) should be written on the top of the file. Can be autocorrected. "
    )
}


class Messages:
    """Contains warnings and their locations. The `set_location()` method
    allows to generate correctly foramtted messages that refer to the correct
    position in the output file.
    """
    # in case your warning is not related with any line this constant should
    # be used in "content" field for explicitly marking it
    NA = 'N/A'

    class Message:
        def __init__(self, warn, anchor, line, kwargs):
            self.warn = warn
            self.anchor = anchor
            self.kwargs = kwargs
            self.line = line

        def __repr__(self):
            return repr(self.__dict__)

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.messages = []
        self.anchor_locations = dict()

    def add(self, anchor, line, warn, **kwargs):
        """ Add a message connected to an achor (i.e. some object representing
        some entity in the source file).
        """

        self.add_anchor(anchor)
        msg = self.Message(warn, anchor, line, kwargs)
        self.messages.append(msg)

    def add_to_file(self, warn, **kwargs):
        """ Add a message connected to the source file itself."""

        self.add(self.filename, self.NA, warn, **kwargs)
        self.set_location(self.filename, -1)

    def add_anchor(self, anchor):
        """ Add an entity which can be referred by a message."""

        self.anchor_locations[anchor] = None

    def __contains__(self, anchor):
        return anchor in self.anchor_locations

    def set_location(self, anchor, lineno):
        """ Set the line number of an anchor."""

        self.anchor_locations[anchor] = lineno

    def show(self):
        """ Print out all saved messages."""

        messages = sorted(self.messages,
                          key=lambda m: self.get_lineno(m.anchor))
        for msg in messages:
            sys.stderr.write('%s\n' % self.__format_msg(msg))

    def __format_msg(self, msg):
        def apply_callable(value):
            if callable(value):
                return value()
            return value

        lineno = self.get_lineno(msg.anchor)
        kwargs = {k: apply_callable(v) for k, v in msg.kwargs.items()}

        warn_dict = dict()
        warn_dict['WARN'] = msg.warn.value
        warn_dict['filename'] = self.filename

        if self.anchor_locations[msg.anchor] >= 0:
            warn_dict['lineno'] = lineno

        warn_dict['message'] = f'{WARNINGS_DESCRIPTION[msg.warn]}'.format(**kwargs)
        if lineno != -1:
            warn_dict['warnline'] = msg.line
        else:
            warn_dict['content'] = self.NA
        # sorting keys here to make output more deterministic
        return json.dumps(warn_dict, sort_keys=True)

    def get_lineno(self, anchor):
        """ Return the location of an anchor."""
        return self.anchor_locations[anchor]
