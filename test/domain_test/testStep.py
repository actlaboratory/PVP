import os
import unittest
import domain

class TestStep(unittest.TestCase):
    def test_ensureStepTypeSupported(self):
        self.assertEqual(domain.ensureStepTypeSupported("InputSingleAudioFile"), "InputSingleAudioFile")
        self.assertRaises(ValueError, domain.ensureStepTypeSupported, "NonexistentStepType")

    def test_isRequired(self):
        step = domain.StepBase(True)
        self.assertTrue(step.isRequired())
        step = domain.StepBase(False)
        self.assertFalse(step.isRequired())

    def test_tryToSetValue(self):
        step = domain.StepBase(True)
        result = step.tryToSetValue("value")
        self.assertTrue(result)
        self.assertEqual(step.getValue(), "value")
        self.assertTrue(step.isValueSet())


class TestInputSingleAudioFileStep(unittest.TestCase):
    def test_validate(self):
        value1 = os.path.join(os.path.dirname(__file__), "__init__.py") # not an audio file but yeah
        value2 = "nonexistent"
        step = domain.InputSingleAudioFileStep(True)
        result1 = step.tryToSetValue(value1)
        self.assertTrue(result1)
        result2 = step.tryToSetValue(value2)
        self.assertFalse(result2.valid)
