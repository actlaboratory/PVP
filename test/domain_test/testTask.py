import os
import unittest
import domain


class TestTask(unittest.TestCase):
    def test_defineRequiredStep(self):
        step = domain.defineRequiredStep(domain.InputSingleAudioFileStep)
        self.assertEqual(step.stepClass, domain.InputSingleAudioFileStep)
        self.assertTrue(step.isRequired)

    def test_defineOptionalStep(self):
        step = domain.defineOptionalStep(domain.InputSingleAudioFileStep)
        self.assertEqual(step.stepClass, domain.InputSingleAudioFileStep)
        self.assertFalse(step.isRequired)


class TestMakeTweetableAudioTask(unittest.TestCase):
    def test_construct(self):
        task = domain.MakeTweetableAudioTask()
        self.assertEqual(len(task._steps), 3)
        self.assertEqual(task._steps[0].stepType(), "InputSingleAudioFile")
        self.assertTrue(task._steps[0].isRequired())
        self.assertEqual(task._steps[1].stepType(), "InputSingleImageFile")
        self.assertTrue(task._steps[1].isRequired())
        self.assertEqual(task._steps[2].stepType(), "OutputTweetableVideoFile")
        self.assertTrue(task._steps[2].isRequired())

    def test_validate(self):
        msgs = [
            '入力: 音声ファイルを1つ選択 のステップが完了していません。',
            '入力: 画像ファイルを1つ選択 のステップが完了していません。',
            '出力: Twitter用動画の保存先を指定 のステップが完了していません。',
        ]
        task = domain.MakeTweetableAudioTask()
        messages = task.validate()
        self.assertEqual(messages, msgs)

    def test_markAsCanceled(self):
        task = domain.MakeTweetableAudioTask()
        self.assertFalse(task.isCanceled())
        task.markAsCanceled()
        self.assertTrue(task.isCanceled())


class TestCutVideoTask(unittest.TestCase):
    def test_construct(self):
        task = domain.CutVideoTask()
        self.assertEqual(len(task._steps), 3)
        self.assertEqual(task._steps[0].stepType(), "InputSingleVideoFile")
        self.assertTrue(task._steps[0].isRequired())
        self.assertEqual(task._steps[1].stepType(), "ShowVideoEditor")
        self.assertTrue(task._steps[1].isRequired())
        self.assertEqual(task._steps[2].stepType(), "OutputSingleVideoFile")
        self.assertTrue(task._steps[2].isRequired())

    def test_getInputFileName(self):
        task = domain.CutVideoTask()
        task.nthStep(1)._value = "test.mp4" # force
        self.assertEqual(task.getInputFileName(), "test.mp4")

    def test_getPrerequisite(self):
        task = domain.CutVideoTask()
        task.nthStep(1)._value = "test.mp4"
        marker = domain.CutMarker(
            startPoint=10000,
            endPoint=20000,
        )
        task.nthStep(2)._value = [marker]
        prereq = task.getPrerequisites()
        self.assertEqual(len(prereq), 1)
        self.assertEqual(prereq[0].path, os.path.join(os.getcwd(), "temp\\concats\\test_parts.txt"))
