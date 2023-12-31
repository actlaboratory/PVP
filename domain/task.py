import os
from .step import *
from .prerequisite import *
from .tempdir import *

if '_' not in globals():
    globals()['_'] = lambda x: x

# TaskStepDefinition defines each step in a task
class TaskStepDefinition:
    def __init__(self, stepClass, isRequired):
        self.stepClass = stepClass
        self.isRequired = isRequired


# defineRequiredStep defines a step which must be configured
def defineRequiredStep(stepClass):
    return TaskStepDefinition(stepClass, True)

# defineOptionalStep defines a step which can be configured but not required
def defineOptionalStep(stepClass):
    return TaskStepDefinition(stepClass, False)


# Task represents an actual task
# A task is generated from a task definition
class TaskBase:
    identifier = None
    _stepDefinitions = []

    def __init__(self):
        self._canceled = False
        self._steps = []
        for s in self._stepDefinitions:
            self._steps.append(s.stepClass(s.isRequired))

    def numberOfSteps(self):
        return len(self._steps)

    def nthStep(self, n):
        # convert to 0-based index
        return self._steps[n - 1]

    def validate(self):
        messages = []
        messages.extend(self._ensureRequiredSteps())
        return messages

    def markAsCanceled(self):
        self._canceled = True

    def isCanceled(self):
        return self._canceled

    def _ensureRequiredSteps(self):
        messages = []
        for s in self._steps:
            if s.isRequired() and not s.isValueSet():
                messages.append(_("%s のステップが完了していません。") % s.stepDescription())
            # end if
        # end for
        return messages

    def _ensureOneOf(self, stepIndexes):
        for i in stepIndexes:
            if self._steps[i].isValueSet():
                return []
            # end if
        # end for
        descriptions = [self._steps[i].stepDescription() for i in stepIndexes]
        return [_("%s のうち、どれか一つを入力してください。") % "、".join(descriptions)]

    def getInputFileName(self):
        return None # override this method to return input file name

    def getOutputFileName(self):
        return None

    def getPrerequisites(self):
        return [] # override this method if the task has prerequisites

class MakeTweetableAudioTask(TaskBase):
    identifier = "MakeTweetableAudio"
    _stepDefinitions = [
        defineRequiredStep(InputSingleAudioFileStep),
        defineRequiredStep(InputSingleImageFileStep),
        defineRequiredStep(OutputTweetableVideoFileStep),
    ]

    def validate(self):
        messages = super().validate()
        return messages


class CutVideoTask(TaskBase):
    identifier = "CutVideo"
    _stepDefinitions = [
        defineRequiredStep(InputSingleVideoFileStep),
        defineRequiredStep(ShowVideoEditorStep),
        defineRequiredStep(OutputSingleVideoFileStep),
    ]

    def validate(self):
        messages = super().validate()
        return messages

    def getInputFileName(self):
        return self.nthStep(1).getValue()

    def getPrerequisites(self):
        cutMarkers = self.nthStep(2).getValue()
        inputDir = os.path.join(tempdirRoot(), "concats")
        inputFileName = os.path.basename(self.getInputFileName()).split(".")[0]
        inputExtention = os.path.basename(self.getInputFileName()).split(".")[1]
        numFiles = len(cutMarkers) + 1
        if len(cutMarkers) > 0 and cutMarkers[-1].endPoint == None:
            numFiles -= 1
        # end if
        content = []
        for i in range(numFiles):
            fn = os.path.join(inputDir, "%s_part%d.%s" % (inputFileName, i+1, inputExtention)).replace("'", "\\'")
            content.append("file '%s'" % fn)
        # end for
        content.append("")
        prerequisite = FilePrerequisite(os.path.join(tempdirRoot(), "concats", "%s_parts.txt" % inputFileName), "\n".join(content))
        return [prerequisite]
