"""
    This module provides a way to run a command in the background and get notified when it's finished.
    It assumes that the program ran by this module is ffmpeg.
    It uses "q" to terminate ffmpeg gracefully.
    To avoid pipe buffer overflow and deadlock, it receives a log file path and writes ffmpeg's stdout and stderr to the file.
    The log file is named like "yyyymmdd_hhmmss_1.log" and is stored in the "logs" directory under the current directory.
    the last number is incremented if the file already exists.
"""

import datetime
import os
import subprocess
import threading
import time
from .os import OSOperation


class CmdResult:
    def __init__(self, identifier, logFilePath, returncode, exception=None):
        self.identifier = identifier
        self.logFilePath = logFilePath
        self.returncode = returncode
        self.exception = exception

class CmdRunner(threading.Thread):
    def __init__(self, identifier, cmd, logFilePath, onFinished = None, osOperation = OSOperation()):
        super().__init__()
        self._identifier = identifier
        self.osOperation = osOperation
        self.cmd = cmd
        self._logFilePath = logFilePath
        self._result = None
        self._onFinished = onFinished
        self._cancelled = False

    def run(self):
        try:
            outfile = self.osOperation.open(self._logFilePath, "w")
            popen = self.osOperation.popen(
                self.cmd,
                stdin=subprocess.PIPE,
                stdout=outfile,
                stderr=outfile,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            while popen.poll() is None:
                time.sleep(0.1)
                if self._cancelled:
                    # Assuming that ffmpeg can be gracefully terminated by sending "q" to stdin
                    # popen.communicate(b'q') does not work
                    popen.stdin.write(b'q')
                    popen.stdin.flush()
                    popen.communicate()
                    break
                # end if
            # end while
            outfile.close()
            self._result = CmdResult(self._identifier, self._logFilePath, popen.returncode)
            if self._onFinished and not self._cancelled:
                self._onFinished(self.result())
            # end if
        except BaseException as e:
            self._result = CmdResult(self._identifier, None, None, e)
            if self._onFinished:
                self._onFinished(self.result())
            # end if

    def logFilePath(self):
        return self._logFilePath

    def result(self):
        return self._result

    def cancel(self):
        self._cancelled = True


def makeLogFilePath(tempDirectory, timestamp, sequenceNumber):
    return os.path.join(
        tempDirectory,
        "logs",
        "%s_%d.log" % (
            timestamp.strftime("%Y%m%d_%H%M%S"),
            sequenceNumber
        )
    )


def ensureUniqueLogFilePath(tempDirectory, timestamp, osOperation = OSOperation()):
    sequenceNumber = 1
    logFilePath = makeLogFilePath(tempDirectory, timestamp, sequenceNumber)
    while osOperation.fileExists(logFilePath):
        sequenceNumber += 1
        logFilePath = makeLogFilePath(tempDirectory, timestamp, sequenceNumber)
    # end while
    return logFilePath


def runCmdInBackground(identifier, cmd, timestamp, onFinished = None, osOperation = OSOperation()):
    logFilePath = ensureUniqueLogFilePath(
        "temp",
        timestamp,
        osOperation
    )
    runner = CmdRunner(identifier, cmd, logFilePath, onFinished, osOperation)
    runner.start()
    return runner

