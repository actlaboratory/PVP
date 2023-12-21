"""
Provides a class for various OS-specific operations.
I'm wrapping these functions here so that I can mock them in tests.
"""

class OSOperation:
    def fileExists(self, path):
        return os.path.exists(path)
