"""
Prerequisites are additional files or special operations which will be needed for certain ffmpeg command.
Currently, the one I'm thinking of is the file list text file for concat command.
Prerequisite classes only defines what is needed, and does not actually do the job.
"""


class FilePrerequisite:
    def __init__(self, path, content):
        self.path = path
        self.content = content

