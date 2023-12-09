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
        self.assertEqual(len(task._steps), 4)
        self.assertEqual(task._steps[0].stepType(), "InputSingleAudioFile")
        self.assertTrue(task._steps[0].isRequired())
        self.assertEqual(task._steps[1].stepType(), "InputPresetImage")
        self.assertFalse(task._steps[1].isRequired())
        self.assertEqual(task._steps[2].stepType(), "InputSingleImageFile")
        self.assertFalse(task._steps[2].isRequired())
        self.assertEqual(task._steps[3].stepType(), "OutputTweetableVideoFile")
        self.assertTrue(task._steps[3].isRequired())

    def test_validate(self):
        msgs = [
            '入力: 音声ファイルを1つ選択 のステップが完了していません。',
            '出力: Twitter用動画の保存先を指定 のステップが完了していません。',
            '入力: プリセットから画像を選択、入力: 画像ファイルを1つ選択 のうち、どれか一つを入力してください。'
        ]
        task = domain.MakeTweetableAudioTask()
        messages = task.validate()
        self.assertEqual(messages, msgs)