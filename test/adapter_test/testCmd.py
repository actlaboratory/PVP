import datetime
import queue
import unittest
from unittest.mock import MagicMock
import adapter
import domain


class TestCmd_success(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        dummyFile = MagicMock()
        dummyPopen = MagicMock()
        dummyPopen.poll.return_value = 0
        dummyPopen.returncode = 0
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.open.return_value = dummyFile
        ope.popen.return_value = dummyPopen
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground("cat task", cmd, timestamp, self.onFinished, ope)
        runner.join()
        result = runner.result()
        self.assertEqual(result.identifier, "cat task")
        self.assertEqual(result.logFilePath, "temp\\logs\\20231201_000000_1.log")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.exception, None)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.identifier, "cat task")
        self.assertEqual(resultFromQueue.logFilePath, "temp\\logs\\20231201_000000_1.log")
        self.assertEqual(resultFromQueue.returncode, 0)
        self.assertEqual(resultFromQueue.exception, None)

    def onFinished(self, result):
        self.queue.put(result)


class TestCmd_success_fileExists(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        dummyFile = MagicMock()
        dummyPopen = MagicMock()
        dummyPopen.poll.return_value = 0
        dummyPopen.returncode = 0
        ope = MagicMock()
        ope.fileExists.side_effect = [True, False]
        ope.open.return_value = dummyFile
        ope.popen.return_value = dummyPopen
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground("cat task", cmd, timestamp, self.onFinished, ope)
        runner.join()
        result = runner.result()
        self.assertEqual(result.identifier, "cat task")
        self.assertEqual(result.logFilePath, "temp\\logs\\20231201_000000_2.log")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.exception, None)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.identifier, "cat task")
        self.assertEqual(resultFromQueue.logFilePath, "temp\\logs\\20231201_000000_2.log")
        self.assertEqual(resultFromQueue.returncode, 0)
        self.assertEqual(resultFromQueue.exception, None)

    def onFinished(self, result):
        self.queue.put(result)


class TestCmd_failure(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        dummyFile = MagicMock()
        dummyPopen = MagicMock()
        dummyPopen.poll.return_value = 1
        dummyPopen.returncode = 1
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.open.return_value = dummyFile
        ope.popen.return_value = dummyPopen
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground("cat task", cmd, timestamp, self.onFinished, ope)
        runner.join()
        result = runner.result()
        self.assertEqual(result.identifier, "cat task")
        self.assertEqual(result.logFilePath, "temp\\logs\\20231201_000000_1.log")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.exception, None)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.identifier, "cat task")
        self.assertEqual(resultFromQueue.logFilePath, "temp\\logs\\20231201_000000_1.log")
        self.assertEqual(resultFromQueue.returncode, 1)
        self.assertEqual(resultFromQueue.exception, None)

    def onFinished(self, result):
        self.queue.put(result)


class TestCmd_success_exception(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        dummyFile = MagicMock()
        dummyPopen = MagicMock()
        dummyPopen.poll.return_value = 0
        dummyPopen.returncode = 0
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.open.return_value = dummyFile
        ope.popen.side_effect = OSError("test")
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground("cat task", cmd, timestamp, self.onFinished, ope)
        runner.join()
        result = runner.result()
        self.assertEqual(result.identifier, "cat task")
        self.assertEqual(result.logFilePath, None)
        self.assertEqual(result.returncode, None)
        self.assertIsInstance(result.exception, OSError)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.identifier, "cat task")
        self.assertEqual(resultFromQueue.logFilePath, None)
        self.assertEqual(resultFromQueue.returncode, None)
        self.assertIsInstance(resultFromQueue.exception, OSError)

    def onFinished(self, result):
        self.queue.put(result)


class TestCmd_cancel(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        dummyFile = MagicMock()
        dummyPopen = MagicMock()
        dummyPopen.poll.return_value = None
        dummyPopen.returncode = 1
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.open.return_value = dummyFile
        ope.popen.return_value = dummyPopen
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground("cat task", cmd, timestamp, self.onFinished, ope)
        self.assertRaises(queue.Empty, self.queue.get, block=True, timeout=0.5)
        runner.cancel()
        runner.join()
        result = runner.result()
        self.assertEqual(result.identifier, "cat task")
        self.assertEqual(result.logFilePath, "temp\\logs\\20231201_000000_1.log")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.exception, None)

    def onFinished(self, result):
        self.queue.put(result)


class TestPrepareCmdRunner(unittest.TestCase):
    def test_prepareCmdRunner(self):
        chain = domain.CommandChain()
        set1 = domain.CommandSet()
        command1 = domain.Command(["test", "-meow"])
        set1.addCommand(command1)
        set2 = domain.CommandSet()
        command21 = domain.Command(["test", "-meow", "-21"])
        command22 = domain.Command(["test", "-meow", "-22"])
        set2.addCommand(command21)
        set2.addCommand(command22)
        chain.addCommandSet(set1)
        chain.addCommandSet(set2)
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.getLogger.return_value = MagicMock()
        runners = adapter.prepareCmdRunners(chain, timestamp, None, ope)
        self.assertEqual(len(runners), 2)
        self.assertEqual(len(runners[0]), 1)
        self.assertEqual(len(runners[1]), 2)


class TestCmd_runCmdChainInBackground(unittest.TestCase):
    def test_runCmdChainInBackground(self):
        chain = domain.CommandChain()
        set1 = domain.CommandSet()
        command1 = domain.Command(["test", "-meow"])
        set1.addCommand(command1)
        set2 = domain.CommandSet()
        command21 = domain.Command(["test", "-meow", "-21"])
        command22 = domain.Command(["test", "-meow", "-22"])
        set2.addCommand(command21)
        set2.addCommand(command22)
        chain.addCommandSet(set1)
        chain.addCommandSet(set2)
        timestamp = datetime.datetime(2023, 12, 1, 0, 0, 0, 0)
        popen = MagicMock()
        popen.poll.return_value = 0
        ope = MagicMock()
        ope.fileExists.return_value = False
        ope.getLogger.return_value = MagicMock()
        ope.popen.return_value = popen
        ope.open.return_value = MagicMock()
        self.eachQueue = queue.Queue()
        self.entireQueue = queue.Queue()
        runner = adapter.runCmdChainInBackground(chain, timestamp, self.onEachCmdFinished, self.onEntireTaskFinished, ope)
        runner.join()
        entireFinished = self.entireQueue.get(block=True, timeout=1)
        self.assertTrue(entireFinished)
        self.assertEqual(self.eachQueue.qsize(), 3)

    def onEachCmdFinished(self, result):
        self.eachQueue.put(result)

    def onEntireTaskFinished(self):
        self.entireQueue.put(True)
