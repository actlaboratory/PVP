from .step import *

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
    _stepDefinitions = []

    def __init__(self):
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

    def _ensureRequiredSteps(self):
        messages = []
        for s in self._steps:
            if s.isRequired() and not s.isValueSet():
                messages.append("%s のステップが完了していません。" % s.stepDescription())
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
        return ["%s のうち、どれか一つを入力してください。" % "、".join(descriptions)]


class MakeTweetableAudioTask(TaskBase):
    _stepDefinitions = [
        defineRequiredStep(InputSingleAudioFileStep),
        defineOptionalStep(InputPresetImageStep),
        defineOptionalStep(InputSingleImageFileStep),
        defineRequiredStep(OutputTweetableVideoFileStep),
    ]

    def validate(self):
        messages = super().validate()
        messages.extend(self._ensureOneOf([1, 2]))
        return messages

