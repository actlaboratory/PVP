from .task import *

# TaskDefinition defines a task supported by this software
class TaskDefinition:
    def __init__(self, taskClass, displayName, description):
        self.taskClass = taskClass
        self.displayName = displayName
        self.description = description

    def generateNewTask(self):
        return self.taskClass()


# Defines a list of supported tasks in this software
supportedTasks = [
    TaskDefinition(
        MakeTweetableAudioTask,
        "音声ファイルをTwitter投稿",
        "音声ファイルからTwitter投稿用の動画ファイルを作成します。",
    )
]
