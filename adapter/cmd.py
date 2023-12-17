import subprocess
import threading
import time

runnerFunc = subprocess.Popen

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
        self._cancelled = False

    def run(self):
        try:
            popen = runnerFunc(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while popen.poll() is None:
                time.sleep(0.05)
                if self._cancelled:
                    popen.send_signal(subprocess.signal.CTRL_C_EVENT)
                    break
                # end if
            # end while
            stdout, stderr = popen.communicate()
            self._result = CmdResult(stdout, stderr, popen.returncode)
            if self._onFinished and not self._cancelled:
                self._onFinished(self.result())
            # end if
        except BaseException as e:
            self._result = CmdResult(None, None, None, e)
            if self._onFinished:
                self._onFinished(self.result())
            # end if

    def result(self):
        return self._result

    def cancel(self):
        self._cancelled = True


def runCmdInBackground(cmd, onFinished = None):
    runner = CmdRunner(cmd, onFinished)
    runner.start()
    return runner

def test_modifyRunnerFunc(newRunnerFunc):
    global runnerFunc
    runnerFunc = newRunnerFunc
