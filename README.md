All rights on the original code are reserved and belong to Google Inc. This fork of original [yapf code](https://github.com/google/yapf) contains new customized code and also Licensed under the Apache License, Version 2.0. 

Thanks to a perfect tool YAPF: https://github.com/google/yapf, it has helped a lot in implementing the below standard.
This fork contains customization of YAPF for Huawei code style. 

Unfortunately yapf is very monolith itself and needs changes in hardcoded logic when you want to change some behavior.

We all hope that one day we will merge at least some changes from this repo to original repo.


# How to build it for windows
1. Install `pyinstaller` : https://www.pyinstaller.org/

2. `pyinstaller $PATH_TO_DIRECTORY_WITH_YAPF\huawei-yapf\yapf\__main__.py --name "huawei-yapf" -F`

3. Use `dist\huawei-yapf.exe`

# How to use it
that will print all styles and all configurations available:
`$ huawe-yapf.exe --style-help` 

# To see all available rules use:
$ huawei-yapf.exe --style-help

Run with default Huawei code style
$ Huawei-yapf.exe $SOME_YOUR_DIR_WITH_PYTHON

# How to use only one inspection (with others disabled)
Default style with no extra changes: `based_on_style: pep8 column_limit: 0 save_initial_indents_formatting: true save_initial_blanklines: true disable_splitting_by_semicolon: true`
For example we are trying to run: `should_have_encoding_header`
`$ huawei-yapf.exe --style="{ based_on_style: pep8 column_limit: 0 save_initial_indents_formatting: true save_initial_blanklines: true disable_splitting_by_semicolon: true should_have_encoding_header: true }"` $SOME_YOUR_DIR_WITH_PYTHON


# Huawei Python Coding Style Guide

## Huawei Technologies Co., Ltd. All Rights Reserved.


# Contents

| **Chapter**              |  **Content**                                                     |
| --------------------- | ------------------------------------------------------------- |
| [0 About This Document](# About This Document)        | [Purpose](# Purpose) [Intended Audience](# Intended Audience) [Scope](# Scope) [Terms & Definitions](# Terms & Definitions) |
| [1 Typesetting](# Typesetting)        | [Indentation](#C1_1) [Statements](#C1_2) [Spaces](#C1_3) [Import](#C1_4) [Interpreters](#C1_5) |
| [2 Comments](# Comments)       |  [Classes, Interfaces, and Functions](#C2_1) [Attributes](#C2_2)  [Formats](#C2_3) [Recommendations](#C2_4)          |
| [3 Naming](# Naming)       | [Packages and Modules](#C3_1) [Classes](#C3_2) [Functions](#C3_3) [Variables](#C3_4) [Recommended Naming Rule Table](#C3_5)                 |
| [4 Coding](# Coding)       | [Coding](# Coding)                  |
| [5 Exceptions](# Exceptions)   |  [Exception Handling](#C5_1) [Assertions](#C5_2)                |
| [6 Concurrency and Parallelism](# Concurrency and Parallelism)       | [Threads](#C6_1)                   |
| [7 Performance](# Performance)       | [Performance](# Performance)                          |
| [8 Programming Practices](# Programming Practices)   |  [Programming Practices](# Programming Practices)              |
| [Appendix](# Appendix)         | [Reference](# Reference) [Contributors](# Contributors) |


# About This Document

## Purpose
Programming is a creative job. 
This specification is used as a guide for software developers to grow up good programming habits and to help developers to 
write consistent, easy-to-read, high-quality code, so it will improve product competitiveness software development efficiency.
This Guide describes common programming issues including program errors, low efficiency, and difficult to maintain, for the code style requirements, coding, exception handling, concurrency and parallelism, and performance in Python language programming.

## Intended Audience

This Guide is intended for developers and test engineers who use the Python language.

## Scope

This Guide is applicable to product development using Python.
Unless otherwise specified, all code examples are based on Python 3.6 or later.

## Terms & Definitions

**Rule**: a convention that must be followed during programming

**Note**: an explanation of a rule

**Recommendation**: a convention that should be followed during programming

**Non-compliant code example**: a code example that violates a rule

**Compliant code example**: a code example that follows a rule

**Exception**: a scenario where the corresponding rules are inapplicable

**Trust boundary**: a boundary within which a system directly controls all components All connections and data from uncontrolled external systems, including clients and third-party systems, should be considered untrusted and verified at the boundary before being allowed to further interact with the system.

**Untrusted code**: code that is excluded in a product package, for example, code that is downloaded, loaded, and executed on a local VM

# <span id="Typesetting">1. Typesetting</span>

## <span id="C1_1">Indentation</span>

## Rule 1.1 <span id="P1_1">A program block is indented by four spaces.</span>

**Note**: A program block is indented by four spaces, which is a universal standard of the industry.

**Non-compliant code example**: The number of spaces is not 4.
```python
def load_data(dirname, one_hot=False):
     X_train = [] # five spaces
     Y_train = [] # five spaces
```
**Compliant code example**:
```python
def load_data(dirname, one_hot=False):
    X_train = []
    Y_train = []
```
## Rule 1.2 <span id="P1_2">Do not simultaneously use spaces and tabs.</span>

**Note**: Only using spaces is recommended for indentation. Only using tabs is allowed. If the existing code contains spaces and tabs, these tabs must be all converted into spaces.

**Non-compliant code example**: Spaces and tabs are simultaneously used.
```python
def load_data(dirname, one_hot=False):
	X_train = [] # tabs
    Y_train = []
```
**Compliant code example**:
```python
def load_data(dirname, one_hot=False):
    X_train = []
    Y_train = []
```
## Rule 1.3 <span id="P1_3">Tabs in new projects must be replaced with spaces.</span>

**Non-compliant code example**: Tabs are used in new projects.
```python
def load_data(dirname, one_hot=False):
	X_train = [] # tabs
	Y_train = [] # tabs
```
**Compliant code example**:
```python
def load_data(dirname, one_hot=False):
    X_train = []
    Y_train = []
```

## <span id="C1_2">Statements</span>

## Rule 1.4 <span id="P1_4">Python files must use UTF-8 encoding.</span>

**Note**: Python files must use UTF-8 encoding (Python 2.x uses ASCII encoding by default).
Files that use ASCII or UTF-8 encoding must have encoding declarations.
Using escape character \\x is a preferred method to include non-ASCII data in a string.

## Rule 1.5 <span id="P1_5">Only one statement can be written in a line.</span>

**Note**: Only one statement can be written in a line. If multiple statements are written in a line, step-by-step debugging cannot be performed for these statements.

**Non-compliant code example**: Multiple statements are written in a line, which makes step-by-step debugging impossible.
```python
rect.length = 0; rect.width = 0;
```
**Compliant code example**:
```python
rect.length = 0
rect.width = 0
```
## Rule 1.6 <span id="P1_6">A blank line must be added between mutually separated program blocks.</span>

**Note**: Adding a blank line between mutually separated program blocks can enhance code readability.

**Non-compliant code example**: No blank line is added between program blocks.
```python
if len(deviceName) < _MAX_NAME_LEN:
……
writer = LogWriter()
```
**Compliant code example**:
```python
if len(deviceName) < _MAX_NAME_LEN:
……

writer = LogWriter()
```

## Recommendation 1.7 <span id="P1_7">Each line contains less than 80 characters to keep consistent with the Python standard library.</span>

**Note**: It is recommended that a development team use the code check tool of its product line or YAPF (https://github.com/google/yapf) to automatically format the code, or use the formatting function of the IDE to uniformly format the code, and then submit the formatted code.

Long statements, expressions, or parameters (\> 80 characters) should be written in multiple lines and should preferentially choose break point in brackets including braces {}, square brackets \[\], and parentheses (). It is recommended that backslashes (\\) be used to break lines. Long expressions should be divided into new lines at a low-priority operator. An operator should be uniformly placed at the beginning of a new line or the end of the original line. A new line shall be properly indented to make the layout uniform and consistent and statements readable.

**Non-compliant code example**: One line contains excessive characters. Reading code is inconvenient.
```python
if width == 0 and height == 0 and color == 'red' and emphasis == 'strong' and
highlight > 100:
    x = 1
```
**Compliant code example**:
```python
if width == 0 \
    and height == 0 \
    and color == 'red' \
    and emphasis == 'strong' \
    and highlight > 100:
    x = 1
```
## <span id="C1_3">Spaces</span>

## Rule 1.8 <span id="P1_8">When more than two keywords, variables, and constants are used for peer operations, spaces must be added at the beginning and end of an operator among the preceding keywords, variables, and constants.</span>

**Note**: Writing the code in this way is to make the code clear.

If multiple spaces need to be added to a long statement, the long statement should be clear as a whole and should partially have no spaces. Do not consecutively add more than one space for an operator.

1. Spaces can be added only after commas (,) and semicolons (;) (if used).

**Non-compliant code example**:
```python
print(a,b , c)
```
**Compliant code example**:
```python
print(a, b, c)
```
2. Binary operators including comparison operators (">", ">=", "<", "=<", "=="),
assignment operators ("=", "+="), arithmetic operators ("+", "-", "%"), and logical operators ("and",
"or") are provided with spaces at the beginning and the end.

**Non-compliant code example**:
```python
if current_time>= MAX_TIME_VALUE:
a=b+ c
a+=2
```
**Compliant code example**:
```python
if current_time >= MAX_TIME_VALUE:
a = b + c
a += 2
```
## Recommendation 1.9 <span id="P1_9">If non-peer operations are performed for immediate operators (for example, "."), no spaces should be added after the immediate operators.</span>

1. For the default value of a parameter in a function definition statement, it is not recommended that spaces be added at the beginning and end of equal signs ("=") used when a function is called and a parameter is passed.
```python
def create(self, name=None)
    self.create(name="mike")
```
2. When "\*" and "\*\*" are used as operators, no spaces are added at the beginning and end of these operators.
**Non-compliant code example**:
```python
a = b * c
a = c ** b
```
**Compliant code example**:
```python
a = b*c
a = c**b
```
3. No spaces are added at the beginning and end of immediate operators (".").
**Non-compliant code example**:
```python
result. writeLog()
```
**Compliant code example**:
```python
result.writeLog()
```
4. No spaces need to be added in one parenthesis, before the close parenthesis, and after the open parenthesis. No spaces must be added in multiple parentheses.
**Non-compliant code example**:
```python
a = ( (b + c)*d - 5 )*6
```
**Compliant code example**:
```python
a = ((b + c)*d - 5)*6
```
5. No space is added before the open square bracket of an index slice or the open parenthesis of a called function name.
**Non-compliant code example**:
```python
dict [key] = list [index]
conn = Telnet.connect (ipAddress)
```
**Compliant code example**:
```python
dict[key] = list[index]
conn = Telnet.connect(ipAddress)
```

## <span id="C1_4">Import</span>

## Rule 1.10 <span id="P1_10">Statements used for loading modules must be separated and written in one line.</span>

**Note**: Statements used for loading modules are written in one line to make program dependency clear.

**Non-compliant code example**:
```python
import sys, os
```
**Compliant code example**:
```python
import sys
import os
```

## Rule 1.11 <span id="P1_11">Imports are added after module comments and docstrings and before the global variable and constant declarations of a module.</span>

**Note**: During the import of libraries, standard libraries, third-party libraries, and local specific libraries or programs should be successively imported. Grouped statements should be separated by blank lines.

**Compliant code example**:
```pyton
import sys
import os

from oslo_config import cfg
from oslo_log import log as logging

from cinder import context
from cinder import db
```

## Recommendation 1.12 <span id="P1_12">Do not import all members in a module by executing the "from xxx import *" statement. </span>
**Note**:
By executing the "from xxx import \*" statement, all members in other modules are assigned to variables with the same name in the current scope. If variables with the same name already exist in the current scope, they are overwritten by default. This method may cause name conflicts, and the conflicts cannot be easily located. Therefore, this method should not be used.

**Compliant code example**:
If yyy needs to be used, execute the "from xxx import yyy" statement.

## <span id="C1_5">Interpreters</span>

## Recommendation 1.13 <span id="P1_13">Use #!/usr/bin/env python in the Python file header that is directly executed in the Unix-like operating system to specify an interpreter.</span>

**Note**: When the hashbang declaration "#!/usr/bin/env python" is used in the Unix-like operating system, the first Python interpreter specified in the PATH variable of the system executes the script. This helps you correctly specify the interpreter for executing Python files. The hashbang declaration should be placed before the file encoding declaration.
This recommendation can be ignored for the Windows operating system.



# <span id="Comments">2. Comments</span>

## <span id="C2_1">Classes, Interfaces, and Functions</span>

## Rules 2.1 <span id="P2_1">Class and interface comments must be written in the next line of the line where the class declaration (class ClassName:) is located and indented by four spaces.</span>

**Note**: Function description contains class or interface functions and relationships with other classes or interfaces. The attribute list includes description about the interface method of the class. The change history includes the modifier, date, and content.

**Compliant code example**:
```python
class TreeError(libxmlError):
    """
    Function Description:
    Interface:
    Change History:
    """
```

## Rule 2.2 <span id="P2_2">Common function comments are written in the next line of the line where the function declaration (def FunctionName(self):) is located and indented by four spaces.</span>

**Note**: Common function comments include the function description, input parameters, output parameters, return values, calling relationships (functions and tables), exception description, and change history. The exception description must describe exception meaning and specify the conditions in which exceptions are thrown, besides exceptions thrown from functions.

**Compliant code example**:
```python
def load_batch(fpath):
    """
    Function Description:
    Parameter:
    Return Value:
    Exception Description:
    Change History
    """
```

## <span id="C2_2">Attributes</span>

## Rule 2.3 <span id="P2_3">Common attribute comments are written above the attribute declaration and have the same indentation as the declaration. Each inter-line comment should start with \# and a space and should be separated by a space from its following text comment.</span>

**Note**: Inter-line comments are defined to add comments in the line above the statement line. Inter-line comments should be less added. Each inter-line comment should start with \# and a space.

**Non-compliant code example**:
```python
#Compensate for border
x = x + 1
```
**Compliant code example**:
```python
# Compensate for border
x = x + 1
```

## <span id="C2_3">Formats</span>

## Rule 2.4 <span id="P2_4">Module comments are written on top of a file and before imports and are not indented.</span>

**Note**: The change history including the modifier, date, and content should be recorded after each modification of the module code.

**Compliant code example**:

```python
"""
Function: XXX class. This class mainly involves the XXX function.
Copyright Information: Huawei Technologies Co., Ltd. All Rights Reserved © 2010-2017
Change History: 2015-03-17 12:00 XXX XXXXXXXX Created
2017-03-17 12:00 XXX XXXXXXXX Modified XXX
"""
```

## Rule 2.5 <span id="P2_5">If a document character string occupies more than one line, """ at the end of the string must be written in another line.</span>

**Note**: If a document character string only occupies one line, """ can be in the line.

**Non-compliant code example**:
```python
"""Return a foobang
Optional plotz says to frobnicate the bizbaz first."""
```
**Compliant code example**:
```python
"""Return a foobang
Optional plotz says to frobnicate the bizbaz first.
"""
```
**Compliant code example**:
```python
"""API for interacting with the volume manager."""
```

## Rule 2.6 <span id="P2_6">Comments must be made above and close to the described code and have the same indentation as the code.</span>

**Note**: Comments should be made close to the described code and have the same indentation as the code. Code comments should be made above and close to the code.

**Non-compliant code example**: Comments do not have the same indentation as the described code.
```python
    # get replicate sub system index and net indicator
repssn_ind = ssn_data[index].repssn_index
repssn_ni = ssn_data[index].ni
```
**Compliant code example**:
```python
# get replicate sub system index and net indicator
repssn_ind = ssn_data[index].repssn_index
repssn_ni = ssn_data[index].ni
```
**Compliant code example**:
```python
if image_service is not None:
    # Deletes the image if it is in queued or saving state
    self._delete_image(context, image_meta['id'], image_service)
```

## <span id="C2_4">Recommendations</span>

## Recommendation 2.7 <span id="P2_7">Comments should be clear to prevent ambiguity.</span>

**Note**: Incorrect comments mislead readers. Comments should be accurate and have no ambiguity. The code should be clearly commented.

## Recommendation 2.8 <span id="P2_8">Do not use abbreviations in comments.</span>

**Note**: Abbreviations should be described before being used or during their use.

## Recommendation 2.9 <span id="P2_9">Synchronously modify the code and comments.</span>

**Note**: Comment the code when writing it. First update the code comments before modifying the code to ensure the consistency between the comments and the code. Delete unnecessary comments.

## Recommendation 2.10 <span id="P2_10">Meaningful variables should be commented.</span>

**Note**: Variables that have physical meanings and whose naming is not fully self-commented must be commented and their physical meanings must be described during declarations. Variable comments should be made above and close to variables.

**Non-compliant code example**:
```python
# No comments are added.
_MAX_ACT_TASK_NUMBER = 1000
```
**Compliant code example**:
```python
# maximum number of active statistic tasks
_MAX_ACT_TASK_NUMBER = 1000
```
## Recommendation 2.11 <span id="P2_11">Global variables should be commented in detail.</span>

**Note**: Detailed comments should be added for each global variable, including the functionality, value range, modification functions or procedures, and precautions on access.

# <span id="Naming">3. Naming</span>

## <span id="C3_1">Packages and Modules</span>

## Rule 3.1 <span id="P3_1">A package or module name has a full meaning and is named by lower_with_under.</span>

**Note**: Modules should be named in the style of lowercases and underscores (_), for example, lower_with_under.py. Although existing modules are named like CapWords.py, this naming is not recommended because a confusion comes if a module has the same name as a class.

**Compliant code example**:
```python
from sample_package import sample_module
from sample_module import SampleClass
```

## <span id="C3_2">Classes</span>
## Rule 3.2 <span id="P3_2">A class name has a full meaning and is named by CapWords.</span>

**Note**: Classes are named in the CapWords style that is commonly used in object-oriented languages.

**Compliant code example**:
```python
class SampleClass(object):
    pass
```

## <span id="C3_3">Functions</span>
## Rule 3.3 <span id="P3_3">A function, method, or function parameter has a full meaning and is named by lower_with_under.</span>

**Note**:
Functions and methods are named in the style of lowercases and underscores (\_), which differs from that of classes.
Function parameters are named in the style of lowercases and underscores (\_), which is the same as that of common variables.
The names of functions used in modules start with a single underscore (\_), indicating that the functions are protected (these functions are excluded when the "from module1 import \*" statement is executed).

**Compliant code example**:
```python
def sample_public_function(sample_parameter):
    pass

def sample_internal_function(sample_parameter):
    pass

class SampleClass(object):

    def sample_member_method(self, sample_parameter):
        pass
```

## <span id="C3_4">Variables</span>
## Rule 3.4 <span id="P3_4">Variables are named in the style of lowercases and underscores (\_), for example, lower\_with\_under. Constants are named in the style of uppercases and underscores (\_), for example, CAPS_WITH_UNDER.</span>

**Note**:

Constants are named in the style of uppercases and underscores (\_), which differs from that of variables.

**Compliant code example**:
```python
sample_global_variable = 0
M_SAMPLE_GLOBAL_CONSTANT = 0

class SampleClass(object):

    SAMPLE_CLASS_CONSTANT = 0

    def sample_member_methond(self, sample_parameter):
        pass

def sample_function():
    sample_function_variable = 0
    sample_instant_variable = SampleClass()

```

## Rule 3.5 <span id="P3_5">The names of private members of classes or objects start with a single underscore (\_). To distinguish a basic class member to be inherited from a derived class member, the basic class member name can start with double underscores (\_\_). </span>

**Note**:
Python has no strict private access control. The industry commonly uses the following method: The member name starts with a single underscore (\_) to indicate that this member is for internal use only. A member name starting with double underscores (\_\_) is automatically renamed by the interpreter and has a class name as its prefix to prevent name conflicts in class inheritance scenarios, not to control the access. In addition, the member name can still be externally accessed. The member name should be used only in scenarios where name conflicts need to be avoided, for example, designing an inherited tool base class.

**Compliant code example**:
```python
class MyClass:
    def my_func(self):
        self._member = 1    # starts with a single underscore (_), indicating that this member should be used only for internal operations of classes and should not be externally accessed.

    def _my_private_func(self):   # starts with a single underscore (_), indicating that this method should be used only for internal operations of classes and should not be externally accessed.
        pass

class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)    # starts with double underscores (__) and can be renamed _Mapping__update by the interpreter. Modified names can also be externally accessed.

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # does not conflict with the name of a derived class member as a private duplicate member used by the update method.

class MappingSubclass(Mapping):
    # has the same name as the base class method. Although the number of parameters is modified, base class __init__ is not affected.
    def update(self, keys, values):
        for item in zip(keys, values):
            self.items_list.append(item)

    __update = update   # does not conflict with base class members because it is renamed _MappingSubclass__update by the interpreter.
```
Reference: https://docs.python.org/3/tutorial/classes.html#private-variables

## Recommendation 3.6 <span id="P3_6">A variable name should have a clear meaning and use a complete word or an abbreviation that can be understood.</span>

**Note**:

1. If special conventions or abbreviations are used in naming, comments are recommended.
2. Any variables except local loop variables cannot be named a single character, for example, i, j, or k.
3. Do not use a single character l or o as the variable name. It is difficult to distinguish characters from digits in some fonts, for example, l and 1, o and 0. If you need to use l as the variable, use L to replace it.

**Non-compliant code example**:
```python
class SampleClass(object):
    pass

def sample_function(sample_parameter):
    i = SampleClass()
    o = [l for l in range(1)]
```
**Compliant code example**:
```python
class SampleClass(object):
    pass

def sample_function(sample_parameter):
    sample_inst = SampleClass()
    number_list = [i for i in range(10)]
```

## <span id="C3_7">Recommended Naming Rule Table</span>
## Recommendation 3.7 <span id="P3_7">Recommended Naming Rule Table</span>
Naming rules recommended by Guido van Rossum, "Father of Python"

| **Type**           | **Public**           | **Internal**              |
|--------------------|----------------------|---------------------------|
| Modules            | lower_with_under     | _lower_with_under         |
| Packages           | lower_with_under     |                           |
| Classes            | CapWords             |                           |
| Exceptions         | CapWords             |                           |
| Functions          | lower_with_under()   | _lower_with_under()       |
| Global/Class Constants | CAPS_WITH_UNDER  | _CAPS_WITH_UNDER          |
| Global/Class Variables | lower_with_under | lower_with_under          |
| Instance Variables     | lower_with_under | lower_with_under (protected) or __lower_with_under (private)  |
| Method Names       | lower_with_under()   | _lower_with_under() (protected) or __lower_with_under() (private) |
| Function/Method Parameters    | lower_with_under |                    |
| Local Variables	 | lower_with_under     |                           |

# <span id="Coding">4. Coding</span>

## Rule 4.1 <span id="P4_1">Compared with None, a value must use the operator "is" or "is not" instead of equal signs ("==").</span>

**Note**:

"is": Identifies whether to point to the same object (whether both object IDs are equivalent). "==": Identifies whether both object values are equivalent by calling the __eq__ method.

**Example**:

For the same instance, the results identified using "is" and "==" are different.
```
>>> class Bad(object):
        def __eq__(self, other):
            return True
>>> bad_inst = Bad()
>>> bad_inst == None
True
>>> bad_inst is None
False
```

## Recommendation 4.2 <span id="P4_2">When \_\_all\_\_ is defined, not all the contents of this module are exposed. The names of variables, functions, and classes that allow external access should be added to \_\_all\_\_.</span>

**Note**:

After \_\_all\_\_ is defined in the module, when the "from module import \*" statement is executed, only the contents defined in \_\_all\_\_ are imported.

**Example**:

sample_package.py
```python
__all__ = ["sample_external_function"]

def sample_external_function():
    print("This is an external function..")

def sample_internal_function():
    print("This is an internal function..")

```

main.py
```python
from sample_package import *

if __name__ == "__main__":
    sample_external_function()
    sample_internal_function()

NameError: name 'sample_internal_function' is not defined
```

## Recommendation 4.3 <span id="P4_3">Do not obtain values from dict using dict\[key\]. If required, pay attention to capturing and processing exceptions when keys do not exist in dict.</span>

**Note**:

Keys in Python dict can be used to obtain the key values. However, if keys are excluded in the key value list of dict, KeyError is reported when dict[key] is used to obtain key values. The more secure method dict.get(key) should be used to obtain values.

**Non-compliant code example**:
```python
sample_dict = {'default_key': 1}
sample_key = 'sample_key'
sample_value = sample_dict[sample_key]
```

**Compliant code example**:
```python
sample_dict = {'default_key': 1}
sample_key = 'sample_key'
sample_value = sample_dict.get(sample_key)
```

## Recommendation 4.4 <span id="P4_4">Do not slice a sequence using a negative step value.</span>

**Note**:

Python provides the sample_list[start : end : stride] format to implement step cutting, that is, extracting one from X elements. X is a variable, which is equivalent to stride. However, if the stride value is negative, the code is difficult to be understood and errors may occur in specific scenarios.

**Non-compliant code example**:

In the following format, the negative stride is used when start : end : stride is used, which makes reading difficult. In this case, it is recommended that the "step" cutting process be separated from the "range" cutting process to make the code clear.
```
>>> a = [1,2,3,4,5,6,7,8]
>>> a[2::2]
[3,5,7]
>>> a[-2::-2]
[7,5,3,1]
>>> a[-2:2:-2]
[7,5]
>>> a[2:2:-2]
[]
```

## Recommendation 4.5 <span id="P4_5">After instance type parameters are passed, call the isinstance function to check the parameters. Do not use the type function.</span>

**Note**: If a type is provided with the factory function, the factory function can be used to covert the type; otherwise, the isinstance function can be used for checking. After instance type parameters are passed using function or method parameters, the isinstance function should be used to check the parameters. Other methods, such as
is not None and len(para) != 0, are insecure.

**Non-compliant code example**:

The following function protection fails to complete the check. If a tuple is input, the protection code can be easily bypassed, causing an execution exception.
```
>>> def sample_sort_list(sample_inst):
...     if sample_inst is []:
...         return
...     sample_inst.sort()
>>> fake_list = (2,3,1,4)
>>> sample_sort_list(fake_list)
Traceback (most recent call last):
  File "<pyshell#232>", line 1, in <module>
    sample_sort_list(fake_list)
  File "<pyshell#230>", line 4, in sample_sort_list
    sample_inst.sort()
AttributeError: 'tuple' object has no attribute 'sort'
```
**Compliant code example**:

Use "isinstance" function to check the input parameters. After the check, execute the "raise exception" or "return" statement as required.
```
>>> def sample_sort_list(sample_inst):
...     if not isinstance(sample_inst, list):
...         raise TypeError(r"sample_sort_list in para type error %s" % type(sample_inst))
...     sample_inst.sort()
>>> fake_list = (2,3,1,4)
>>> sample_sort_list(fake_list)
Traceback (most recent call last):
  File "<pyshell#235>", line 1, in <module>
    sample_sort_list(fake_list)
  File "<pyshell#234>", line 3, in sample_sort_list
    raise TypeError(r"sample_sort_list in para type error %s" % type(sample_inst))
TypeError: sample_sort_list in para type error <type 'tuple'>
```

## Recommendation 4.6 <span id="P4_6">Create a sequence through comprehension instead of repeated logical operations. The code readability must be considered for comprehension. It is not recommended that list comprehension with more than two expressions be used.</span>

**Note**:

Comprehension is a refined sequence generation method. This method can be used to complete simple logics and is recommended in scenarios where sequences are generated. However, if logics are complex (more than
two logical expressions), this method is not mandatory because it makes the code readability poor.

**Non-compliant code example**:

The following code uses a simple logic, but it has a loop and is complex. Therefore, performance is poor.
```python
odd_num_list = []
for i in range(100):
    if i % 2 == 1:
        odd_num_list.append(i)
```
**Compliant code example**:
```python
odd_num_list = [i for i in range(100) if i % 2 == 1]
```
Using list comprehension achieves simple logics and makes the code clear and refined.

## Recommendation 4.7 <span id="P4_7">The function code should be encapsulated in functions or classes.</span>

**Note**: In Python, when a module is imported, all the top-level code is executed,
and misoperations, such as calling functions and creating objects, are easily caused. Therefore, the code should be encapsulated in functions or classes. It is recommended that if __name__ == '__main__'  be checked for the script code before the main program is executed.
In this way, the main program is not executed when a module is imported.

**Compliant code example**:
```python
def main():
    ...

if __name__ == '__main__':
    main()
```

## Recommendation 4.8 <span id="P4_8">The decimal module should be used in scenarios where accurate value calculation is required.</span>

**Note**: In Python, do not use floating point numbers to create Decimal because floating point numbers are inaccurate.

**Compliant code example**:
```
>>> from decimal import Decimal
>>> Decimal('3.14')
Decimal('3.14')
>>> getcontext().prec = 6
>>> Decimal(1) / Decimal(7)
Decimal('0.142857')
```
**Non-compliant code example**:
```
>>> from decimal import Decimal
>>> getcontext().prec = 28
>>> Decimal(3.14)
Decimal('3.140000000000000124344978758017532527446746826171875')
```

## Rule 4.9 <span id="P4_9">Do not use the same variable name for different objects.</span>

**Note**:
Python is a weakly typed language. It allows assigning different types of objects to the same variable. However, this assignment may lead to a runtime error. The code complexity is increased and the code is hard to be debugged and maintained due to semantic changes of the variable context, and performance is not improved.

**Non-compliant code example**
```python
items = 'a,b,c,d' # character strings
items = items.split (',') # changed to a list
```

**Compliant code example**
```python
items = 'a,b,c,d' # character strings
itemList = items.split (',') # changed to a list
```

## Rule 4.10 <span id="P4_10">If instances do not need to be accessed when the class method is used, use @staticmethod or @classmethod for decoration based on scenarios.</span>

**Note**:
In the class method, the received self parameter is the class instance. However, instances do not need to be accessed in some methods. Two cases are as follows:
1. Any member does not need to be accessed, or only the class members need to be explicitly accessed. This method does not require additional parameters and should be decorated using @staticmethod.
In Python 3.x, the method that directly defines parameters excluding the self parameter is allowed, and the method can be called without instances. If the method is called through instances, an error occurs due to parameter mismatching.
Using @staticmethod for decoration provides better readability because the Python interpreter confirms that the self parameter is not needed in this method and intercepts errors.

**Non-compliant code example**:
```python
class MyClass:
    def my_func():    # not decorated using @staticmethod. An error occurs when this method is used through instances.
        pass

MyClass.my_func()    # allowed in Python 3.x. An error occurs in Python 2.x.
my_instance = MyClass()
my_instance.my_func()   # Errors occur in both Python 3.x and 2.x.
```
**Compliant code example**:
```python
class MyClass:
    @staticmethod
    def my_func():     # After being decorated using @staticmethod, this method is parsed by the interpreter into a static method.
        pass

MyClass.my_func()    # OK
my_instance = MyClass()
my_instance.my_func()   # OK, not recommended because this method is easily confused with common methods. MyClass.my_func() is recommended.
```
2. Instance members do not need to be accessed, but base class or derived class members need to be accessed. This method should be decorated using @classmethod. In the decorated method, the bottom-layer class of a caller, rather than an instance is passed to the first parameter.
In the following code example, the count method of the base class Spam is used to count the number of instances of each class in the inheritance tree.
```python
class Spam:
    numInstances = 0
    @classmethod
    def count(cls):    # Independently counts each class.
        cls.numInstances += 1    # cls is the bottom-layer class of instances.
    def __init__(self):
        self.count()    # Outputs self.__class__ to the count method.

class Sub(Spam):
    numInstances = 0

class Other(Spam):
    numInstances = 0

x = Spam()
y1, y2 = Sub(), Sub()
z1, z2, z3 = Other(), Other(), Other()
x.numInstances, y1.numInstances, z1.numInstances    # output: (1, 2, 3)
Spam.numInstances, Sub.numInstances, Other.numInstances    # output: (1, 2, 3)
```
However, when @classmethod is used, note that the first parameter in the inheritance scenario is not necessarily the class itself. Therefore, @classmethod should not be used in all access class member scenarios. For example, a Base class explicitly wants to modify its member inited (rather than a derived class member). In this case, @staticmethod should be used.

**Non-compliant code example**:
```python
class Base:
    inited = False
    @classmethod
    def set_inited(cls):   # A Derived class may be input.
        cls.inited = True    # Base.inited is not modified, but members are added to the Derived class.

class Derived(Base):
    pass

x = Derived()
x.set_inited()
if Base.inited:
    print("Base is inited")   # is not executed.
```

## Recommendation 4.11 <span id="P4_11">Modules in each directory should be managed in packages when multiple Python source code files are stored in different subdirectories. </span>
**Note**:
Including the \_\_init\_\_.py file in a subdirectory can make the Python code use the subdirectory as the package name in the "import" and "from" statements, and manage each module by layer to make the relationship between modules clear. The \_\_init\_\_.py file can contain initialization actions required by the package and also define the \_\_all\_\_ list to specify modules that are included in the "from \*" statement. For a package that does not need to be initialized, only store an empty file named \_\_init\_\_.py in a directory to identify that the directory is a package.

**Compliant code example**:
Assume that the root directory of the Python source code is dir0, the root directory contains the subdirectory dir1, dir1 contains the subdirectory dir2, and dir2 contains the mod.py module,
store the \_\_init\_\_.py file in dir1 and dir2, and use the mod.py module in other code as follows:
```python
import dir1.dir2.mod
dir1.dir2.mod.func()    # calls the func function in the mod.py module.

from dir1.dir2.mod import func    # adds the func function to the current scope.
func()    # called directly without the package name and the module name.
```

## Recommendation 4.12 <span id="P4_12">Do not modify the sys.path list in the code.</span>
**Note**:
sys.path is the module search path used when the Python interpreter executes the "import" and "from" statements. It is composed of the current directory, system environment variables, library directories, and .pth file configurations. By modifying system configurations, specify the module search path. Module search path sys.path should be generated based only on user system configurations and should not be modified in the code. Otherwise, sys.path may be modified by module A, making module B fails to be searched, and the user is hard to locate the fault.

**Compliant code example**:
To add a module search path, modify the environment variable PYTHONPATH. If subdirectories need to be managed, modules should be organized by package.

## Recommendation 4.13 <span id="P4_13">Process set data in an iterative manner by executing the "for x in iterable" statement instead of the "for i in range(x)" statement.</span>
**Note**:
The "for i in range(x)" statement is a habit of C language programming to obtain elements using the subscript [i] for sets in a loop body. It has the following disadvantages: It is easy to exceed the boundary; an error occurs when i is modified in a loop body; the readability is poor. The "for x in iterable" statement is recommended for Python, that is, taking each piece of data from sets for processing.

**Non-compliant code example**:
```python
for i in range(len(my_list)):
    print(my_list[i])
```
**Compliant code example**:
```python
for x in my_list:
    print(x)
```
In some cases, the serial number of each element needs to be used during processing. The built-in function enumerate can be called to number elements to form a tuple.
```python
my_list = ['a', 'b', 'c']
for x in enumerate(my_list):
    print(x)
```
The output is as follows:
(0, 'a')
(1, 'b')
(2, 'c')

## Rule 4.14 <span id="P4_14">Do not use duplicate names in irrelevant variables or concepts to avoid accidental assignment and incorrect reference.</span>
**Note**:
Compared with the C language, Python has different function or class definitions. The function or class definition statement is used to assign a name. Repeatedly defining a function or class name does not lead to an error because the repeated definition overwrites the previous one. However, repeated definitions can easily hide coding errors, that is, the meaning of a function or class with the same name may vary with the executing phase. This reduces readability and should be prohibited.
When parsing a referenced name, Python follows the sequence of the LEGB rule: Local->Enclosed->Global->Built-in and searches for the name from a small scope to a large scope. Variables defined in the small scope overwrite those with the same name in the large scope. During code modification, variables with the same name should not be used because they may lead to incorrect reference and reduce code readability.

# <span id="Exceptions">5. Exception Handling</span>

## <span id="C5_1">Exception Handling</span>

## Rule 5.1 <span id="P5_1">When using try…except… to protect the code, use finally… to ensure that operation objects are released after an exception occurs.</span>

**Note**:

When using try…except… to protect the code, if an exception occurs during code execution, use finally… to ensure that operation objects can be released.

**Example**:
```python
handle = open(r"/tmp/sample_data.txt")  # May raise IOError
try:
    data = handle.read()  # May raise UnicodeDecodeError
except UnicodeDecodeError as decode_error:
    print(decode_error)
finally:
    handle.close()  # Always run after try:
```

## Rule 5.2 <span id="P5_2">Do not capture all exceptions by executing the "except:" statement.</span>

**Note**:

In case of exceptions, Python executes the "except:" statement to capture any errors including Python syntax errors. Executing the "except:" statement hides potential bugs. Therefore, specify exceptions to be handled when using try…except… to protect the code.
The Exception class is the base class of most runtime exceptions and should not be used in the "except:" statement. The "try" statement should contain only exceptions that must be handled at the current location. The "except:" statement should only captures exceptions that must be handled. For example, for the code for opening files, the "try" statement should contain only the "open" statement. The "except:" statement only captures the FileNotFoundError exception. Other unexpected exceptions are captured by functions in the upper layer, or are transparently transmitted to external programs for exposure.

**Non-compliant code example**:

Two types of exceptions may occur in the following code. They are uniformly handled by executing the "except:" statement. If "open" statement execution exceptions occur and the handle variable after the "except:" statement is invalid, the close method is called and an error that the handle variable is invalid is reported.
```python
try:
    handle = open(r"/tmp/sample_data.txt")  # May raise IOError
    data = handle.read()  # May raise UnicodeDecodeError
except:
    handle.close()
```
**Compliant code example**:
```python
try:
    handle = open(r"/tmp/sample_data.txt")  # May raise IOError
    try:
        data = handle.read()  # May raise UnicodeDecodeError
    except UnicodeDecodeError as decode_error:
        print(decode_error)
    finally:
        handle.close()

except(FileNotFoundError, IOError) as file_open_except:
    print(file_open_except)
```

## Rule 5.3 <span id="P5_3">The raise keyword that is not contained in the "except:" statement must have exceptions specified.</span>

**Note**: The raise keyword can be used only in the "try-except" statement and re-throw exceptions captured by the "except:" statement.

**Non-compliant code example**:
```
>>> a = 1
>>> if a==1:
...     raise
...
Traceback (most recent call last):
File "<stdin>", line 2, in <module>
TypeError: exceptions must be old-style classes or derived from BaseException, not NoneType
```
**Compliant code example 1**: Raise an Exception or a custom Exception.
```
>>> a = 1
>>> if a==1:
...     raise Exception
...
Traceback (most recent call last):
File "<stdin>", line 2, in <module>
Exception
```
**Compliant code example 2**: Use the raise keyword in the "try-except" statement.
```
>>> import sys
>>>
>>> try:
...     f = open('myfile.txt')
...     s = f.readline()
...     i = int(s.strip())
... except IOError as e:
...     print("I/O error({0}): {1}".format(e.errno, e.strerror))
... except ValueError:
...     print("Could not convert data to an integer.")
... except:
...     print("Unexpected error:", sys.exc_info()[0])
...     raise
```

## Recommendation 5.4 <span id="P5_4">Use exceptions to express special cases, not to return None.</span>

When you use a tool method, None is returned to express a special meaning. For example, when a number is divided by another number, if the dividend is 0, return None to indicate that there is no result.
```python
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

result = divide(x, y)
if result is None:
    print('Invalid inputs')

```
What will be returned if the numerator is 0? The value 0 is returned (if the denominator is not 0). The preceding code is ignored when being checked in the if condition. The if condition is used to not only check whether the value is None, but also add all False conditions to the code.
```python
x, y = 0, 5
result = divide(x, y)
if not result:
    print('Invalid inputs') # This is wrong!

```
The preceding information is common in the Python coding process and explains that the method of returning None is undesirable. The preceding error can be handled using the following two types of methods:

1. Change the return value to a tuple. The first part indicates whether the operation is successful, and the second part is the actual return value (similar to processing in the Go language).

```python
def divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None
```

In this method, obtain and unpack the return value, and check the first part, not only check the result.
```python
success, result = divide(x, y)
if not success:
    print('Invalid inputs')
```

This method brings another problem: The method user easily ignores the first part (use _ to identify unused variables in Python) of the tuple. This code is actually the same as that containing None.
```python
_, result = divide(x, y)
if not result:
    print('Invalid inputs')

```

2. Trigger an exception to enable the user to handle, that is, triggering ValueError to package the existing error ZeroDivisionError and remind the user that the input parameters are incorrect. This method is recommended.

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

```

In this case, the user must handle the exception caused by the incorrect input parameters (the exception should be commented). The user does not need to check the return value because the return value is correct when an exception is not thrown. Exceptions are clearly handled.

```
x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)
>>>
Result is 2.5

```
Remember:
(1) The method of using None as the return value with a special meaning is not recommended for coding because None and other return values must be added with extra check code.
(2) If identifying special cases by triggering exceptions, the user captures and handles exceptions.

## Recommendation 5.5 <span id="P5_5">Do not use the "return" or "break" statement in the finally code block.</span>

Using the "finally" statement indicates that some resources need to be released. In this case, the try, except, and else code blocks have been executed. If an exception is triggered during the execution and is not handled, it is temporarily stored and re-triggered after the finally code block is executed. However, if the finally code block contains the **return** or **break** statement, the exception is discarded.

```python
def f():
    try:
        1/0
    finally:
        return 42

print(f())
```

After the preceding code is executed, an exception generated by the "1/0" statement is ignored, and the return value is 42. Therefore, the "return" statement is undesirable in the finally code block.

When the ''return", "break", and "continue" statements are executed in the try code block, the finally code block is also executed.

```python
def foo():
    try:
        return 'try'
    finally:
        return 'finally'


>>> foo()
'finally'
```

The output is incorrect because the "return" and "break" statements are incorrectly used.

## Rule 5.6 <span id="P5_6">Use syntax except X as x instead of except X, x.</span>
**Note**:
Syntax except X, x is supported only in Python 2.x and is unsupported in Python 3.x for compatibility. This syntax is easily confused with a tuple expression that can be used to capture multiple exceptions. Therefore, the syntax should be uniformly named except X as x.

## <span id="C5_2">Assertions</span>

## Recommendation 5.7 <span id="P5_7">Use the "assert" statement only in the test code instead of production versions.</span>

The **assert** statement is used to declare that a condition is true. For example, if you want to verify that a list contains at least one element and trigger an exception when the condition is untrue, the **assert** statement is the best choice. When the **assert** statement does not pass the verification, an **AssertionError** exception is triggered.

```
>>> mylist = ['item']
>>> assert len(mylist) >= 1
>>> mylist.pop()
'item'
>>> assert len(mylist) >= 1
Traceback (most recent call last): File "<stdin>", line 1, in ? AssertionError
```
The **assert** statement is executed only for internal tests in the R&D process. If an **AssertionError** exception occurs, the software design or code is incorrect. The software should be modified. Do not include the **assert** function in externally released production versions.

# <span id="Concurrency and Parallelism">6. Concurrency and Parallelism</span>

## <span id="C6_1">Multithreading applies to blocking I/O scenarios instead of parallel computing scenarios.</span>

The standard implementation of Python is CPython.

CPython executes the Python code in two steps: 1. Compile the text source code interpretation into bytecode; 2. Use an interpreter to parse the running bytecode. The bytecode interpreter is stateful and its status consistency needs to be maintained. Therefore, the Global Interpreter Lock (GIL) is used.

With the GIL, CPython cannot use multiple CPUs to improve computing efficiency when executing the multi-threaded code, because only one thread runs at a time. This feature brings the following benefit: When CPython runs multiple threads, internal objects are thread-safe by default. Python library developers benefit from this. However, when CPython developers want to remove the GIL, they find that a large number of code libraries heavily depend on the benefit brought by the GIL.

Although multithreading does not deliver benefits in parallel computing scenarios, it can improve efficiency in blocking I/O scenarios. This is because blocking I/O threads can be suspended when performing I/O operations without the CPU time occupied in blocking I/O scenarios. Non-I/O operations of other threads can use the CPU time. In this way, multi-threaded parallel I/O operations can improve running efficiency.

In a word, only one thread runs at a time, and CPython cannot use multiple CPUs to improve computing efficiency due to the existence of GIL. Therefore, multithreading of Python is applicable to blocking I/O scenarios rather than parallel computing scenarios.

To verify that the multithreading of Python does not apply to parallel computing scenarios, the following uses an example of a code instance that has a requirement about the amount of calculation and factorizes a number:
```python
# -*- coding:utf-8 -*-
from time import time
from threading import Thread


def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


class FactorizeThread(Thread):
    def __init__(self, number):
        Thread.__init__(self)
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


def test(numbers):
    start = time()
    for number in numbers:
        list(factorize(number))
    end = time()
    print('Took %.3f seconds' % (end - start))


def test_thread(numbers):
    start = time()
    threads = []
    for number in numbers:
        thread = FactorizeThread(number)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
    end = time()
    print('Mutilthread Took %.3f seconds' % (end - start))


if __name__ == "__main__":
    numbers = [2139079, 1214759, 1516637, 1852285]

    test(numbers)
    test_thread(numbers)

```
The code output is as follows:
```
Took 0.319 seconds
Mutilthread Took 0.539 seconds
```
The execution result of the preceding code is for reference only. The specific value varies with the running environment. However, we can see that the code computing speed in single-thread mode is faster than that in multi-thread mode. Only one thread runs at a time due to the existence of GIL when CPython executes the multi-threaded code. Multi-threaded parallel computing, however, increases total execution time for thread scheduling.

In blocking I/O scenarios, multithreading can be used to schedule other threads to perform non-I/O operations when I/O blocking occurs. Therefore, multithreading can save time. The effect can be verified by executing the following code:
```python
# -*- coding:utf-8 -*-
from time import time
from threading import Thread
import os


def slow_systemcall(n):
    for x in range(100):
        open("test_%s" % n, "a").write(os.urandom(10) * 100000)


def test_io(N):
    start = time()
    for _ in range(N):
        slow_systemcall(_)
    end = time()
    print('Took %.3f seconds' % (end - start))


def test_io_thread(N):
    start = time()
    threads = []
    for _ in range(N):
        thread = Thread(target=slow_systemcall, args=("t_%s"%_,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end - start))


if __name__ == "__main__":
    N = 5
    test_io(N)
    test_io_thread(N)

```
The code output is as follows:
```
Took 5.179 seconds
Multithread Took 1.451 seconds
```
It can be seen that the ratio of the time taken by a single thread to the time taken by multiple threads is close to 1:4. Considering the thread scheduling time, this case is similar to that in which multithreading of common languages works. This is because a system call is executed when Python executes I/O operations. In this case, threads release the GIL. After the system call ends, threads re-apply for the GIL. In other words, threads are concurrently executed during I/O operations.

Another implementation of Python is JPython. JPython does not have the GIL but is not the most common Python implementation.

# <span id="Performance">7. Performance</span>


## Recommendation 7.1 <span id="P7_1">If the number of members in a list is predictable, space should be reserved just for all members during the list creation.</span>

Note: Like the list of the Java and C++ languages, the list of the Python language allocates larger memory to new members added by calling the append() method and copies the original members to the memory to release the original memory. If the append() method is called for many times, the preceding process frequently occurs and performance deteriorates catastrophically.

Non-compliant code example:
```python
members = []
for i in range(1, 1000000):
     members.append(i)
len(members)

```
Compliant code example:
```
members = [None] * 1000000
for i in range(1, 1000000):
     members[i] = i
len(members)

```
## Recommendation 7.2 <span id="P7_2">Replace lists with tuples in scenarios where the number and contents of members remain unchanged.</span>

Note: A list is a dynamic array. A tuple is a static array (the number and contents of members are unchanged). A list needs more memory to trace its member statuses.

Python caches a tuple with 20 or less members. When the tuple is no longer used, Python does not immediately return the memory occupied by the tuple to the system but reserves it for future use.

Non-compliant code example:
```python
myenum = [1, 2, 3, 4, 5]
```
Compliant code example:
```python
myenum = (1, 2, 3, 4, 5)  # If cached, the initialization speed is more than five times that described in the non-compliant code example.
```

## Recommendation 7.3 <span id="P7_3">Replace range with xrange in Python 2.x.</span>

Note: for x in range(1, 10000) in Python is common and is equivalent to for (int i = 0; i \< 10000; i++) in Java, C, or C++. However, range is equivalent to the following definition:
```python
def range(begin, end, step=1):
indices = []
while begin < end:
    indices.append(begin)
    start += step

```
In this process, the indices array may have a low performance, and the cost of using the range function to traverse values is high.
xrange is equivalent to the following definition:
```python
def range(begin, end, step=1):
while begin < end:
    yield begin
    start += step

```
In this process, no large array is generated. Each for loop only receives a value from xrange. Xrange provides and provides only the current value for each for loop. Therefore, the space usage is low. In addition, no operations of allocating new memory, copying the data from the original memory, and releasing the original memory are performed during capacity expansion.

Non-compliant code example:
```python
for x in range(1, 1000000):
    print(x)
```
Compliant code example:
```python
for x in xrange(1, 1000000):
    print(x)
```
## Recommendation 7.4 <span id="P7_4">Replace list comprehension with generator comprehension.</span>

Note: List comprehension can replace the map and reduce syntaxes of the lambda expression to generate new data from the existing list. Generator comprehension can generate a generator without need to define a function that contains the yield statement.
In the two methods, the generation speed is close, but the memory usage is greatly different.

Non-compliant code example:
```python
even_cnt = len([x for x in range(10) if x % 2 == 0])
```
Compliant code example:
```python
even_cnt = sum(1 for x in range(10) if x % 2 == 0)
```

## Recommendation 7.5 <span id="P7_5">Use the format and join methods and the "%" operator in a loop rather than the "+" and "+=" operators to format character strings.</span>

**Note**: Even if parameters are all character strings, the format method or the "%" operator can also be used to format the character strings. In scenarios that have common performance requirements, the "+" or "+=" operator can be used, but character strings can not be accumulated in a loop. Character strings are unchangeable. Therefore, unnecessary temporary objects are generated, and quadratic and non-linear running time is caused.

**Compliant code example**:
```python
x = '%s, %s!' % (imperative, expletive)
x = '{}, {}!'.format(imperative, expletive)
x = 'name: %s; score: %d' % (name, n)
x = 'name: {}; score: {}'.format(name, n)
name = "Fred"
x = f"He said his name is {name}."
items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)
```

**Non-compliant code example**:
```python
x = imperative + ', ' + expletive + '!'
x = 'name: ' + name + '; score: ' + str(n)
employee_table = '<table>'
for last_name, first_name in employee_list:
    employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
employee_table += '</table>'
```

# <span id="Programming Practices">8. Programming Practices</span>

## Rule 8.1 <span id="P8_1">The default value of a variable in function parameters must be set to None.</span>

**Note**: The default value of a parameter has been set when the method definition is executed. This means that the default value is set only once. After a function is defined, it is pre-calculated once being called. If the default value of a parameter is mutable, pre-calculation is more important. For example, if the default parameter value is a list or dict and is modified by calling a method (for example, adding data to the list), this modification affects the next calling of this method. This way is not good. To solve the problem, set the default value of a parameter to None.

**Non-compliant code example**:
```
>>> def foo(bar=[]): # bar is optional and defaults to [] if not specified
...    bar.append("baz") # but this line could be problematic, as we'll see...
...    return bar
```

In the preceding example, once the foo() function is repeatedly called (the bar parameter is not specified), "bar" is returned. This is because the bar parameter is not specified, [] is assigned to it once the foo() function is called. The result is as follows:
```
>>> foo()
["baz"]
>>> foo()
["baz", "baz"]
>>> foo()
["baz", "baz", "baz"]
```

**Compliant code example**:
```
>>> def foo(bar=None):
...    if bar is None:      # or if not bar:
...        bar = []
...    bar.append("baz")
...    return bar
...
>>> foo()
["baz"]
>>> foo()
["baz"]
>>> foo()
["baz"]
```


## Rule 8.2 <span id="P8_2">Do not use comment lines to make the code invalid.</span>

**Note**: The comments of Python include single-line comments, multi-line comments, inter-code comments, and docstrings. Docstrings are multi-line comments enclosed in """""", which are commonly used to describe information about the usage, functionality, parameters, and return value of classes or functions. Other types of comments start with \#, which is used to comment out the contents following \#. If the py file rather than the code is provided, some functions can be enabled by modifying comments due to the Python compilation particularity although some functions and methods are commented in the code. If some interface functions that should have been shielded are not completely deleted from the code, these functions may be enabled without a notice. Therefore, the features, modules, functions, and variables that are not used in Python must be deleted from the code according to the security redline requirements. Even if the compiled pyc and pyo files rather than the py file of the source code are provided, the source code can be obtained through decompilation. This may cause unpredictable results.

**Non-compliant code example**: Two interfaces in the main.py file are commented out but are not deleted.
```
if __name__ == "__main__":
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
        if option == "load":
            # Install an application.
            LoadCmd(option, sys.argv[2:3][0])
        elif option == 'unload':
            # Uninstall the application.
            UnloadCmd(sys.argv[2:3][0])
        elif option == 'unloadproc':
            # Uninstall a process.
            UnloadProcessCmd(sys.argv[2:3][0])
#       elif option == 'active':
#           ActiveCmd(sys.argv[2:3][0])
#       elif option == 'inactive':
#           InActiveCmd(sys.argv[2:3][0])
        else:
            Loginfo("Command %s is unknown"%(sys.argv[1]))
```

In the preceding example, the two shielded interfaces are easily found in the program, which is insecure. The code commented out should be deleted.
```
if __name__ == "__main__":
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
        if option == "load":
            # Install an application.
            LoadCmd(option, sys.argv[2:3][0])
        elif option == 'unload':
            # Uninstall the application.
            UnloadCmd(sys.argv[2:3][0])
        elif option == 'unloadproc':
            # Uninstall a process.
            UnloadProcessCmd(sys.argv[2:3][0])
        else:
            Loginfo("Command %s is unknown"%(sys.argv[1]))
```
## Recommendation 8.3 <span id="P8_3">Cautiously use the copy and deepcopy method.</span>

**Note**: In Python, object assignment is to reference an object. When an object is created and assigned to another variable, Python does not copy the object but copies its reference. To copy an object, use the copy module in a standard library. The copy module provides the following two methods:
- copy (shallow copy): Copy an object, but reference the original attributes of the object. For variable types, such as lists and dictionaries, just copy their references. Reference-based changes affect the referenced objects.
- deepcopy (deep copy): Create a container object, including reference of the copy of the original object elements. For all internal elements, copy their objects, not reference the objects.

Note: The digits, character strings, and other atomic objects are not copied. To reassign an object, only create an object and replace the old one with the new object. Know application scenarios to avoid incorrect use before using the copy and deepcopy methods.

**Example**:

```
>>> import copy
>>> a = [1, 2, ['x', 'y']]
>>> b = a
>>> c = copy.copy(a)
>>> d = copy.deepcopy(a)
>>> a.append(3)
>>> a[2].append('z')
>>> a.append(['x', 'y'])
>>> print(a)
[1, 2, ['x', 'y', 'z'], 3, ['x', 'y']]
>>> print(b)
[1, 2, ['x', 'y', 'z'], 3, ['x', 'y']]
>>> print(c)
[1, 2, ['x', 'y', 'z']]
>>> print(d)
[1, 2, ['x', 'y']]

```


## Rule 8.4 <span id="P8_4">Complete operations related to file system paths using methods provided by the os.path library, not by assembling character strings.</span>

**Note**: The os.path library provides a series of operation methods for file system paths, which are more secure than the method of assembling path character strings and can be used to shield differences among different operating systems for users.

**Non-compliant code example**: Path character strings cannot be assembled in the Linux operating system.
```python
path = os.getcwd() + '\\test.txt'
```

**Compliant code example**:
```python
path = os.path.join(os.getcwd(), 'test.txt')
```

## Recommendation 8.5 <span id="P8_5">Execute the shell command using the subprocess module instead of the os.system module.</span>

**Note**: The subprocess module can generate processes, connect these processes to their input, output, or error function pipelines, and obtain their returned code. This module is designed to replace the os.system module because it is more flexible.

**Compliant code example**:
```python
>>> subprocess.run(["ls", "-l"])  # does not capture output
CompletedProcess(args=['ls', '-l'], returncode=0)

>>> subprocess.run("exit 1", shell=True, check=True)
Traceback (most recent call last):
  ...
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

>>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')
```

## Recommendation 8.6 <span id="P8_6">Operate files by executing the "with" statement.</span>

**Note**: Python adds the support for context managers to some built-in objects, and these objects are used in the "with" statement. The "with'' statement can be used to automatically close files, reducing the possibility of file read code errors and the code volume, and improving code robustness. Note that types (objects) operated by the "with" statement should support \_\_enter\_\_() and \_\_exit\_\_(). If supported, the "with" statement can be used.

**Compliant code example**:
```python
with open(r'somefileName') as somefile:
    for line in somefile:
        print(line)
        # ...more code
```
The code that uses the "with" statement is equivalent to the following code using try...finally...:
```python
somefile = open(r'somefileName')
try:
    for line in somefile:
        print(line)
        # ...more code
finally:
    somefile.close()
```
In terms of the code volume and robustness, the "with" statement is better than try...finally....

# <span id="Appendix">Appendix

## Reference

1. <https://docs.python.org>
2. https://www.python.org/dev/peps/pep-0008/
3. https://docs.python.org/3.7/tutorial/controlflow.html#default-argument-values
4. http://google.github.io/styleguide/pyguide.html
5. Effective Python: 59 Specific Ways to Write Better Python
6. Writing Solid Python Code: 91 Suggestions to Improve Your Python Program

## Contributors
Thanks to all experts and colleagues who have participated in the formulation and review of these rules and recommendations.
