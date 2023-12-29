# ffmpeg command generation

import os
from .duration import *
from .tempdir import *

class CommandChain:
    """
    This class represents a chain of commands.
    It contains a list of command sets.
    Each command set can have multiple commands which can be executed in parallel.
    The next command set must be executed after all of the commands in the previous command set are finished.
    """

    def __init__(self):
        self._commandSets = []

    def addCommandSet(self, set):
        self._commandSets.append(set)

    def nthCommandSet(self, n):
        return self._commandSets[n - 1]

    def countCommandSets(self):
        return len(self._commandSets)


class CommandSet:
    def __init__(self):
        self._commands = []

    def addCommand(self, command):
        self._commands.append(command)

    def nthCommand(self, n):
        return self._commands[n - 1]

    def countCommands(self):
        return len(self._commands)


class Command:
    def __init__(self, command):
        self.command = command


def ensureTaskIdentifier(identifier, expected):
    if identifier != expected:
        raise ValueError("identifier must be %s, got %s" % (expected, identifier))

def makeTweetableAudioCommand(task):
    ensureTaskIdentifier(task.identifier, "MakeTweetableAudio")
    chain = CommandChain()
    command1 = Command(
        [
            "ffmpeg",
            "-i",
            task.nthStep(1).getValue(),
            "-i",
            task.nthStep(2).getValue(),
            "-loop",
            "1",
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-pix_fmt",
            "yuv420p",
            task.nthStep(3).getValue()
        ]
    )
    set = CommandSet()
    set.addCommand(command1)
    chain.addCommandSet(set)
    return chain


def CutVideoCommand(task):
    ensureTaskIdentifier(task.identifier, "CutVideo")
    cutMarkers = task.nthStep(2).getValue()
    if len(cutMarkers) == 0:
        raise ValueError("cutMarkers must not be empty")
    # end if
    cuts = []
    cuts.append((0, cutMarkers[0].startPoint))
    for i in range(len(cutMarkers) - 1):
        cuts.append((cutMarkers[i].endPoint, cutMarkers[i + 1].startPoint))
    # end for
    cuts.append((cutMarkers[-1].endPoint, None))
    chain = CommandChain()
    concatSet = CommandSet()
    inputFile = task.nthStep(1).getValue()
    for cut in cuts:
        cmd = makeCutCommand(inputFile, cut[0], cut[1])
        concatSet.addCommand(cmd)
    # end for
    chain.addCommandSet(concatSet)
    withoutExtension = os.path.basename(inputFile).split(".")[0]
    joinSet = CommandSet()
    joinSet.addCommand(
        Command(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                os.path.join(tempdirRoot(), "concats", "%s_parts.txt" % withoutExtension),
                "-c",
                "copy",
                task.nthStep(3).getValue()
            ]
        )
    )
    chain.addCommandSet(joinSet)
    return chain

def makeCutCommand(input, start, end):
    root = tempdirRoot()
    cmd = [
        "ffmpeg",
        "-i",
        input,
        "-ss",
        millisecondsToPositionStr(start),
    ]
    if end is not None:
        cmd.extend(["-to", millisecondsToPositionStr(end)])
    # end if
    withoutExtension = os.path.basename(input).split(".")[0]
    extension = os.path.basename(input).split(".")[1]
    cmd.extend([
        "-c",
        "copy",
        os.path.join(root, "concats", "%s_part%d.%s" % (withoutExtension, i+1, extension))
    ])
    return Command(cmd)


cmdMap = {
    "MakeTweetableAudio": makeTweetableAudioCommand
}

def generateFfmpegCommand(task):
    return cmdMap[task.identifier](task)
