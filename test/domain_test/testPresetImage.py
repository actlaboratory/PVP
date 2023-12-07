import unittest
import domain

class TestPresetImage(unittest.TestCase):
    def test_isPresetImageAvailable(self):
        self.assertTrue(domain.isPresetImageAvailable("cat"))
        self.assertFalse(domain.isPresetImageAvailable("dog"))
