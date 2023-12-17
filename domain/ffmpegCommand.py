# ffmpeg command generation

def makeTweetableVideoFile(steps):
    return [
        "ffmpeg",
        "-i",
        steps[0].getValue(),
        "-i",
        steps[1].getValue(),
        "-loop",
        "1",
        "-vf",
        "\"scale=trunc(iw/2)*2:trunc(ih/2)*2\"",
        "-pix_fmt",
        "yuv420p",
        steps[2].getValue()
    ]
