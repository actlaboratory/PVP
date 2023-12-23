from .task import *
if '_' not in globals():
    globals()['_'] = lambda x: x

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
        _("音声ファイルをTwitter投稿"),
        _("音声と画像ファイルからTwitter投稿用の動画ファイルを作成します。"),
    )
]
