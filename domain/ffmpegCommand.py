# ffmpeg command generation

import os
from .duration import *
from .tempdir import *


commonFfmpegOptions = [
    "ffmpeg",
    "-y",
]


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
        commonFfmpegOptions + 
        [
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


def cutVideoCommand(task):
    ensureTaskIdentifier(task.identifier, "CutVideo")
    cutMarkers = task.nthStep(2).getValue()
    if len(cutMarkers) == 0:
        raise ValueError("cutMarkers must not be empty")
    # end if
    cuts = []
    if not cutMarkers[0].pointsFileTop():
        cuts.append((millisecondsToPositionStr(0), cutMarkers[0].startPoint))
    # end if
    for i in range(len(cutMarkers) - 1):
        cuts.append((cutMarkers[i].endPoint, cutMarkers[i + 1].startPoint))
    # end for
    if len(cutMarkers) > 0 and cutMarkers[-1].endPoint is not None:
        cuts.append((cutMarkers[-1].endPoint, None))
    # end if
    chain = CommandChain()
    concatSet = CommandSet()
    inputFile = task.nthStep(1).getValue()
    i = 1
    for cut in cuts:
        cmd = makeCutCommand(inputFile, cut[0], cut[1], i)
        concatSet.addCommand(cmd)
        i += 1
    # end for
    chain.addCommandSet(concatSet)
    withoutExtension = os.path.basename(inputFile).split(".")[0]
    joinSet = CommandSet()
    joinSet.addCommand(
        Command(
            commonFfmpegOptions + 
            [
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

def makeCutCommand(input, start, end, part):
    root = tempdirRoot()
    cmd = commonFfmpegOptions + [
        "-i",
        input,
        "-ss",
        start,
    ]
    if end is not None:
        cmd.extend(["-to", end])
    # end if
    withoutExtension = os.path.basename(input).split(".")[0]
    extension = os.path.basename(input).split(".")[1]
    cmd.extend([
        "-c",
        "copy",
        os.path.join(root, "concats", "%s_part%d.%s" % (withoutExtension, part, extension))
    ])
    return Command(cmd)


cmdMap = {
    "MakeTweetableAudio": makeTweetableAudioCommand,
    "CutVideo": cutVideoCommand
}

def generateFfmpegCommand(task):
    return cmdMap[task.identifier](task)
