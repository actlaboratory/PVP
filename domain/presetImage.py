import os

# PresetImage is a class that defines preset image information
class PresetImage:
    def __init__(self, identifier, displayName, imageFilePath):
        self.identifier = identifier
        self.displayName = displayName
        self.imageFilePath = imageFilePath


# Defines preset image information
availablePresetImages  [
    PresetImage("cat", "猫", os.path.join("data", "preset_images", "cat.jpg")),
]


def isPresetImageAvailable(identifier):
    for presetImage in availablePresetImages:
        if presetImage.identifier == identifier:
            return True
        # end if
    # end for
    return False
