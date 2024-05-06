import urllib.request
import os
import shutil
import zipfile

def downloadFFmpeg():
	ffmpegVersion = "6.1.1"
	remoteFile = "ffmpeg-%s-full_build" % ffmpegVersion
	url = "https://github.com/GyanD/codexffmpeg/releases/download/%s/%s.zip" % (ffmpegVersion, remoteFile)
	print("Downloading FFmpeg from %s" % url)
	urllib.request.urlretrieve(url, "ffmpeg.zip")
	print("Extracting FFmpeg...")
	with zipfile.ZipFile("ffmpeg.zip", "r") as zip:
		zip.extract("%s/bin/ffmpeg.exe" % remoteFile)
	# end with
	print("moving ffmpeg.exe to current directory...")
	shutil.move(os.path.join(remoteFile, "bin", "ffmpeg.exe"), "ffmpeg.exe")
	print("removing temporary files...")
	shutil.rmtree(remoteFile)
	os.remove("ffmpeg.zip")
	print("got ffmpeg!")
