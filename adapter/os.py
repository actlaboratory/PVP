"""
Provides a class for various OS-specific operations.
I'm wrapping these functions here so that I can mock them in tests.
"""

import os
import subprocess
from logging import getLogger

class OSOperation:
    def fileExists(self, path):
        return os.path.exists(path)

    def directoryExists(self, path):
        return os.path.isdir(path)

    def open(self, path, mode):
        return open(path, mode, encoding="utf-8")

    def popen(self, args, **kwargs):
        return subprocess.Popen(args, **kwargs)

    def mkdir(self, path):
        return os.mkdir(path)

    def getLogger(self, name):
        return getLogger(name)
