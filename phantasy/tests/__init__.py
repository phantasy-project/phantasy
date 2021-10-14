# -*- coding: utf-8 -*-

import pytest
import os
import shutil

CWD = os.path.dirname(__file__)
TMP_DIR = "/tmp/phantasy_data"

def main():
    """Run tests for `phantasy` package, accept CLI options when executing
    `test_phantasy` command.
    """
    pytest.main([CWD])
    if os.path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    return 0
