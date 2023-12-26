import unittest
from unittest.mock import MagicMock
import adapter
import domain


class TestPrerequisite_filePrerequisite(unittest.TestCase):
    def test_createFilePRerequisite(self):
        filePrerequisite = domain.FilePrerequisite("test.txt", "test! meowww")
        fp = MagicMock()
        fp.__enter__.return_value = fp
        osOperation = MagicMock()
        osOperation.open.return_value = fp
        adapter.createFilePrerequisite(filePrerequisite, osOperation)
        osOperation.open.assert_called_with("test.txt", "w")
        fp.write.assert_called_with("test! meowww")
