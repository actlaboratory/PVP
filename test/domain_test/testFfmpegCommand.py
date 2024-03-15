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
        self.assertEqual(cmd, "ffmpeg -y -i test.mp3 -i test.jpg -loop 1 -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 -pix_fmt yuv420p test.mp4")

    def test_cutVideoCommand(self):
        task = domain.CutVideoTask()
        task.nthStep(1)._value = "test.mp4"
        task.nthStep(2)._value = [
            domain.CutMarker("00:00:01.000", "00:00:02.000"),
        ]
        task.nthStep(3)._value = "test2.mp4"
        chain = domain.cutVideoCommand(task)
        self.assertEqual(chain.countCommandSets(), 2)
        concatDir = os.path.join(os.getcwd(), "temp", "concats")
        set = chain.nthCommandSet(1)
        self.assertEqual(set.countCommands(), 2)
        cmd = " ".join(set.nthCommand(1).command)
        self.assertEqual(cmd, "ffmpeg -y -i test.mp4 -ss 00:00:00.000 -to 00:00:01.000 -c copy %s" % os.path.join(concatDir, "test_part1.mp4"))
        cmd = " ".join(set.nthCommand(2).command)
        self.assertEqual(cmd, "ffmpeg -y -i test.mp4 -ss 00:00:02.000 -c copy %s" % os.path.join(concatDir, "test_part2.mp4"))

    def test_cutVideoCommand_cuttingFromTop(self):
        task = domain.CutVideoTask()
        task.nthStep(1)._value = "test.mp4"
        task.nthStep(2)._value = [
            domain.CutMarker("00:00:00.000", "00:00:02.000"),
        ]
        task.nthStep(3)._value = "test2.mp4"
        chain = domain.cutVideoCommand(task)
        self.assertEqual(chain.countCommandSets(), 2)
        concatDir = os.path.join(os.getcwd(), "temp", "concats")
        set = chain.nthCommandSet(1)
        self.assertEqual(set.countCommands(), 1)
        cmd = " ".join(set.nthCommand(1).command)
        self.assertEqual(cmd, "ffmpeg -y -i test.mp4 -ss 00:00:02.000 -c copy %s" % os.path.join(concatDir, "test_part1.mp4"))
