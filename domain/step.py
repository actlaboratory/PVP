import os

if '_' not in globals():
    globals()['_'] = lambda x: x

# Editing steps

supportedStepTypes = [
    "InputSingleAudioFile",
    "InputSingleImageFile",
    "InputPresetImage",
    "OutputTweetableVideoFile",
    "InputSingleVideoFile",
    "OutputSingleVideoFile",
]

def ensureStepTypeSupported(stepType):
    if stepType not in supportedStepTypes:
        raise ValueError("Unsupported step type: " + stepType)
    # end exception
    return stepType


class InputValidationResult:
    def __init__(self, valid, message, allowForce):
        self.valid = valid
        self.message = message
        self.allowForce = allowForce


def inputValidationOK():
    return InputValidationResult(True, "", True)


class StepBase:
    def __init__(self, isRequired):
        self._value = None
        self._isRequired = isRequired
        self._isValueSet = False

    def stepType(self):
        raise NotImplementedError("you must implement step type method")

    def stepDescription(self):
        raise NotImplementedError("you must implement step description method")

    def isRequired(self):
        return self._isRequired

    def getValue(self):
        return self._value

    def tryToSetValue(self, value, force = False):
        result = self.validateValue(value)
        if not result.valid:
            if not result.allowForce or not force:
                return result
            # end if
        # end if
        self._isValueSet = True
        self._value = value
        return True

    def validateValue(self, value):
        return inputValidationOK()

    def isValueSet(self):
        return self._isValueSet

    def clearValue(self):
        self._value = None

class InputSingleAudioFileStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("InputSingleAudioFile")

    def stepDescription(self):
        return _("入力: 音声ファイルを1つ選択")

    def validateValue(self, value):
        if not os.path.isfile(value):
            return InputValidationResult(False, _("指定されたファイルがありません。"), False)
        # end exception
        return inputValidationOK()


class InputSingleImageFileStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("InputSingleImageFile")

    def stepDescription(self):
        return _("入力: 画像ファイルを1つ選択")

    def validateValue(self, value):
        if not os.path.isfile(value):
            return InputValidationResult(False, _("指定されたファイルがありません。"), False)
        # end exception
        return inputValidationOK()


class OutputTweetableVideoFileStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("OutputTweetableVideoFile")

    def stepDescription(self):
        return _("出力: Twitter用動画の保存先を指定")

    def validateValue(self, value):
        return inputValidationOK()

class InputPresetImageStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("InputPresetImage")

    def stepDescription(self):
        return _("入力: プリセットから画像を選択")

    def validateValue(self, value):
        return inputValidationOK()


class InputSingleVideoFileStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("InputSingleVideoFile")

    def stepDescription(self):
        return _("入力: 動画ファイルを1つ選択")

    def validateValue(self, value):
        if not os.path.isfile(value):
            return InputValidationResult(False, _("指定されたファイルがありません。"), False)
        # end exception
        return inputValidationOK()


class OutputSingleVideoFileStep(StepBase):
    def stepType(self):
        return ensureStepTypeSupported("OutputSingleVideoFile")

    def stepDescription(self):
        return _("出力: 動画の保存先を指定")

    def validateValue(self, value):
        return inputValidationOK()
