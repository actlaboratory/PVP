# ffmpeg command generation

def ensureTaskIdentifier(identifier, expected):
    if identifier != expected:
        raise ValueError("identifier must be %s, got %s" % (expected, identifier))

def makeTweetableAudioCommand(task):
    ensureTaskIdentifier(task.identifier, "MakeTweetableAudio")
    return [
        "ffmpeg",
        "-i",
        task.nthStep(1).getValue(),
        "-i",
        task.nthStep(2).getValue(),
        "-loop",
        "1",
        "-vf",
        "\"scale=trunc(iw/2)*2:trunc(ih/2)*2\"",
        "-pix_fmt",
        "yuv420p",
        task.nthStep(3).getValue()
    ]


cmdMap = {
    "MakeTweetableAudio": makeTweetableAudioCommand
}

def generateFfmpegCommand(task):
    return cmdMap[task.identifier](task)
