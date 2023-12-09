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
        "音声ファイルをTwitterに上げたい",
        "音声ファイルを指定して、Twitterに上げるための動画ファイルを作成します。",
    )
]
