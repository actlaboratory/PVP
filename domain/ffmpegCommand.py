# ffmpeg command generation

class commandChain:
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
    chain = commandChain()
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


cmdMap = {
    "MakeTweetableAudio": makeTweetableAudioCommand
}

def generateFfmpegCommand(task):
    return cmdMap[task.identifier](task)
