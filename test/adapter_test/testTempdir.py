import os
import unittest
from unittest.mock import MagicMock, call
import adapter


class TestTempdir(unittest.TestCase):
    def test_tempdir(self):
        ope = MagicMock()
        ope.directoryExists.return_value = False
        structure = {
            "test": {
                "testInner": {}
            }
        }
        adapter.makeTempdir(structure, [], ope)
        ope.mkdir.assert_has_calls([
            call("test"),
            call(os.path.join("test", "testInner"))
        ])

