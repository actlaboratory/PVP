import subprocess
import unittest
import adapter

class TestFileExists(unittest.TestCase):
    def test_fileExists(self):
        ope = adapter.OSOperation()
        self.assertTrue(ope.fileExists(__file__))
        self.assertFalse(ope.fileExists(__file__ + "nonexistent"))


class TestOpen(unittest.TestCase):
    def test_open(self):
        ope = adapter.OSOperation()
        with ope.open(__file__, "r") as f:
            self.assertNotEqual(f.read(), "")


class TestPopen(unittest.TestCase):
    def test_popen(self):
        ope = adapter.OSOperation()
        p = ope.popen(["python", "--version"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        self.assertEqual(stderr, b"")
        outstr = stdout.decode("utf-8")
        self.assertTrue(outstr.startswith("Python"))
