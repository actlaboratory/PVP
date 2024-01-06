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
import queue
import subprocess
import threading
import time
from .os import OSOperation
import constants


class Timer:
    def __init__(self):
        self.started = datetime.datetime.now()

    def elapsed(self):
        return (datetime.datetime.now() - self.started).total_seconds()


class CmdResult:
    def __init__(self, identifier, logFilePath, returncode, exception=None):
        self.identifier = identifier
        self.logFilePath = logFilePath
        self.returncode = returncode
        self.exception = exception

class CmdRunner(threading.Thread):
    def __init__(
        self,
        identifier,
        cmd,
        logFilePath,
        onFinished = None,
        osOperation = OSOperation(),
    ):
        super().__init__()
        self._identifier = identifier
        self.osOperation = osOperation
        self.cmd = cmd
        self._logFilePath = logFilePath
        self._result = None
        self._onFinished = onFinished
        self._cancelled = False
        self._logger = osOperation.getLogger("%s.CmdRunner.%s" % (constants.LOG_PREFIX, identifier))

    def log(self, msg):
        if self._logger:
            self._logger.debug(msg)
        # end if

    def logElapsed(self, timer):
        self.log("Runner took %.02f seconds" % timer.elapsed())

    def run(self):
        self.log("Preparing to run command: %s" % " ".join(self.cmd))
        timer = Timer()
        try:
            outfile = self.osOperation.open(self._logFilePath, "w")
            self.log("Output file opened: %s" % self._logFilePath)
            popen = self.osOperation.popen(
                self.cmd,
                stdin=subprocess.PIPE,
                stdout=outfile,
                stderr=outfile,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            self.log("Process started: %s" % popen)
            while popen.poll() is None:
                time.sleep(0.1)
                if self._cancelled:
                    # Assuming that ffmpeg can be gracefully terminated by sending "q" to stdin
                    # popen.communicate(b'q') does not work
                    self.log("Cancelling the command")
                    popen.stdin.write(b'q')
                    popen.stdin.flush()
                    popen.communicate()
                    break
                # end if
            # end while
            outfile.close()
            self.log("Process exited with code %d" % popen.returncode)
            self.log("Log file saved to %s" % self._logFilePath)
            self._result = CmdResult(self._identifier, self._logFilePath, popen.returncode)
            self.logElapsed(timer)
            if self._onFinished and not self._cancelled:
                self._onFinished(self.result())
            # end if
        except BaseException as e:
            self.log("Error occurred while running command: %s" % str(e))
            self._result = CmdResult(self._identifier, None, None, e)
            self.logElapsed(timer)
            if self._onFinished:
                self._onFinished(self.result())
            # end if

    def logFilePath(self):
        return self._logFilePath

    def result(self):
        return self._result

    def cancel(self):
        self._cancelled = True

    def identifier(self):
        return self._identifier


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


def prepareCmdRunner(identifier, cmd, timestamp, onFinished = None, osOperation = OSOperation()):
    logFilePath = ensureUniqueLogFilePath(
        "temp",
        timestamp,
        osOperation
    )
    # Touch the log file here. Without this, the same log file path will be used for all runners since tasks are not executed in this preparation step.
    f = osOperation.open(logFilePath, "w")
    f.close()
    runner = CmdRunner(identifier, cmd, logFilePath, onFinished, osOperation)
    return runner


def prepareCmdRunners(chain, timestamp, onEachCmdFinished = None, osOperation = OSOperation()):
    log = osOperation.getLogger("%s.prepareCmdRunners" % constants.LOG_PREFIX)
    runners = []
    for i in range(chain.countCommandSets()):
        setIndex = i + 1
        set = chain.nthCommandSet(setIndex)
        childRunners = []
        for j in range(set.countCommands()):
            cmdIndex = j + 1
            cmd = set.nthCommand(cmdIndex)
            identifier = "step%d.sub%d" % (setIndex, cmdIndex)
            runner = prepareCmdRunner(identifier, cmd.command, timestamp, onEachCmdFinished, osOperation)
            childRunners.append(runner)
            log.debug("Prepared runner: %s" % runner)
        # end for
        runners.append(childRunners)
        log.debug("Prepared %d runners for step %d" % (len(childRunners), setIndex))
    # end for
    return runners


def runCmdInBackground(identifier, cmd, timestamp, onFinished = None, osOperation = OSOperation()):
    logFilePath = ensureUniqueLogFilePath(
        "temp",
        timestamp,
        osOperation
    )
    runner = CmdRunner(identifier, cmd, logFilePath, onFinished, osOperation)
    runner.start()
    return runner


class ChainResult:
    def __init__(self, failures, cancelled):
        self.failures = failures # list of CmdResult
        self.cancelled = cancelled # bool (true if cancelled)


class MultiTaskRunner(threading.Thread):
    # TODO: does not support concurrent execution yet
    def __init__(self, runners, onEntireTaskFinished=None, osOperation=OSOperation()):
        super().__init__()
        self.runners = runners
        self._onEntireTaskFinished = onEntireTaskFinished
        self._cancelled = False
        self.osOperation = osOperation
        self.logger = osOperation.getLogger("%s.MultiTaskRunner" % constants.LOG_PREFIX)
        self._result = None
        self._failures = []

    def run(self):
        self.logger.debug("Starting multi-task runner")
        for set in self.runners:
            for runner in set:
                self.executeCmd(runner)
                if self._cancelled:
                    self.logger.debug("cancelled execution")
                    self._result = ChainResult([], True)
                    break
                # end if
            # end for
        #end for
        if self._cancelled:
            self.logger.debug("cancelled and exiting")
            return
        # end if
        self._result = ChainResult(self._failures, False)
        if self._onEntireTaskFinished:
            self._onEntireTaskFinished(self._result)
        # end if
        self.logger.debug("successfully executed the chain, exiting")

    def executeCmd(self, runner):
        self.logger.debug("Starting command runner: %s" % runner.identifier())
        runner.start()
        while(runner.is_alive()):
            time.sleep(0.1)
            if self._cancelled:
                self.logger.debug("cancelling command runner: %s" % runner.identifier())
                runner.cancel()
                break
            # end if
        # end while
        runner.join()
        result = runner.result()
        if result.returncode != 0 or result.exception:
            self._failures.append(result)

    def cancel(self):
        self.logger.debug("attempting to cancel the chain")
        self._cancelled = True

    def result(self):
        return self._result


def runCmdChainInBackground(chain, timestamp, onEachCmdFinished = None, onEntireTaskFinished = None, osOperation = OSOperation()):
    runners = prepareCmdRunners(chain, timestamp, onEachCmdFinished, osOperation)
    runner = MultiTaskRunner(runners, onEntireTaskFinished, osOperation)
    runner.start()
    return runner
