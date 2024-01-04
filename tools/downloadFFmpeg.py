import os
import sys
sys.path.append(os.getcwd())

from tools import ffmpegDownloader


if os.path.isfile("ffmpeg.exe"):
	print("ffmpeg.exe already exists!")
else:
	ffmpegDownloader.downloadFFmpeg()
# end if
