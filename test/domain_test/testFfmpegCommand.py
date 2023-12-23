import os
import unittest
import domain

class TestFfmpegCommand(unittest.TestCase):
    def test_makeTweetableAudio(self):
        task = domain.MakeTweetableAudioTask()
        task.nthStep(1)._value = "test.mp3"
        task.nthStep(2)._value = "test.jpg"
        task.nthStep(3)._value = "test.mp4"
        chain = domain.makeTweetableAudioCommand(task)
        self.assertEqual(chain.countCommandSets(), 1)
        set = chain.nthCommandSet(1)
        self.assertEqual(set.countCommands(), 1)
        cmd = " ".join(set.nthCommand(1).command)
        self.assertEqual(cmd, "ffmpeg -i test.mp3 -i test.jpg -loop 1 -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 -pix_fmt yuv420p test.mp4")
