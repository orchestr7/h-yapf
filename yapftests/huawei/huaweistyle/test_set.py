import os

from yapf.yapflib import yapf_api, style, file_resources

WINDOWS_EOL = '\r\n'
UNIX_EOL = '\n'


class TestSet:
    def __init__(self):
        # We could as well pass `style_config='huawei'` to `FormatFile()`
        # but configuring via `setUpClass()` is the way used in other tests
        # (such as "reformatter_facebook_test").
        # Besides, even if we did passed `style_config`, `FormatFile()`
        # would call the very same `style.SetGlobalStyle()` inside itself
        # anyway.
        #
        style.SetGlobalStyle(style.CreateHuaweiStyle())

    test_set = set()

    def enrich(self, test_files, test_pattern, expected_pattern):
        for test in test_files:
            test_name_str = os.path.basename(test)
            expected_str = self.__find_corresponding_result(
                test, test_pattern, expected_pattern)
            test_str = yapf_api.FormatFile(test)[0]
            test_str = test_str.replace(WINDOWS_EOL, UNIX_EOL)

            self.test_set.add((test_name_str, test_str, expected_str))

    def __find_corresponding_result(self, test_filename,
                                    test_pattern, expected_pattern):
        """All test files for fixes should have postfixes: INCORRECT or CORRECT.
        All files for testing of warning should have postfixes: WARN or MSG_FILE
         """
        expected_file_path = test_filename.replace(test_pattern,
                                                   expected_pattern)
        with open(expected_file_path, 'r') as file:
            expected_str = file.read()
        # small hack to fix changing of EOL to WIN format
        return expected_str.replace(WINDOWS_EOL, UNIX_EOL)
