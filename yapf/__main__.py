# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main entry point."""
# pylint: disable=invalid-name
import yapf
import sys

# this code is needed for Windows OS to have normal multiprocessing working
# in case when YAPF will be build and distributed as executable (.exe) file
# using pyinstaller. Otherwise it will fail with unrecognized option
# See: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
if sys.platform.upper().startswith('WIN'):
    import multiprocessing
    multiprocessing.freeze_support()

yapf.run_main()
