"""
Provides a class for various OS-specific operations.
I'm wrapping these functions here so that I can mock them in tests.
"""

import os
import subprocess

class OSOperation:
    def fileExists(self, path):
        return os.path.exists(path)

    def open(self, path, mode):
        return open(path, mode)

    def popen(self, args, **kwargs):
        return subprocess.Popen(args, **kwargs)
