import queue
import unittest
import adapter

class DummyExitProcess():
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

def returnSuccess(cmd, stdout, stderr):
    return DummyExitProcess("command succeeded", "", 0)

def returnFailure(cmd, stdout, stderr):
    return DummyExitProcess("", "command failed", 1)

def returnException(cmd, stdout, stderr):
    raise BaseException("exception!")

class TestCmd_success(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        adapter.test_modifyRunnerFunc(returnSuccess)
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground(cmd, self.onFinished)
        runner.join()
        result = runner.result()
        self.assertEqual(result.stdout, "command succeeded")
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.exception, None)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.stdout, "command succeeded")
        self.assertEqual(resultFromQueue.stderr, "")
        self.assertEqual(resultFromQueue.returncode, 0)
        self.assertEqual(resultFromQueue.exception, None)

    def onFinished(self, result):
        self.queue.put(result)

class TestCmd_failure(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        adapter.test_modifyRunnerFunc(returnFailure)
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground(cmd, self.onFinished)
        runner.join()
        result = runner.result()
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "command failed")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.exception, None)
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.stdout, "")
        self.assertEqual(resultFromQueue.stderr, "command failed")
        self.assertEqual(resultFromQueue.returncode, 1)
        self.assertEqual(resultFromQueue.exception, None)

    def onFinished(self, result):
        self.queue.put(result)

class TestCmd_exception(unittest.TestCase):
    def test_runCmdInBackground(self):
        self.queue = queue.Queue()
        adapter.test_modifyRunnerFunc(returnException)
        cmd = ["test", "-meow"]
        runner = adapter.runCmdInBackground(cmd, self.onFinished)
        runner.join()
        result = runner.result()
        self.assertEqual(result.stdout, None)
        self.assertEqual(result.stderr, None)
        self.assertEqual(result.returncode, None)
        self.assertEqual(result.exception.args[0], "exception!")
        resultFromQueue = self.queue.get(block=True, timeout=1)
        self.assertEqual(resultFromQueue.stdout, None)
        self.assertEqual(resultFromQueue.stderr, None)
        self.assertEqual(resultFromQueue.returncode, None)
        self.assertEqual(resultFromQueue.exception.args[0], "exception!")

    def onFinished(self, result):
        self.queue.put(result)
