import subprocess
import threading

runnerFunc = subprocess.run

class CmdResult:
    def __init__(self, stdout, stderr, returncode, exception=None):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.exception = exception

class CmdRunner(threading.Thread):
    def __init__(self, cmd, onFinished = None):
        super().__init__()
        self.cmd = cmd
        self._result = None
        self._onFinished = onFinished

    def run(self):
        try:
            result = runnerFunc(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self._result = CmdResult(result.stdout, result.stderr, result.returncode)
            if self._onFinished:
                self._onFinished(self.result())
            # end if
        except BaseException as e:
            self._result = CmdResult(None, None, None, e)
            if self._onFinished:
                self._onFinished(self.result())
            # end if

    def result(self):
        return self._result

def runCmdInBackground(cmd, onFinished = None):
    runner = CmdRunner(cmd, onFinished)
    runner.start()
    return runner

def test_modifyRunnerFunc(newRunnerFunc):
    global runnerFunc
    runnerFunc = newRunnerFunc
