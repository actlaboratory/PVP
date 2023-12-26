from .os import OSOperation


def createFilePrerequisite(filePrerequisite, osOperation=OSOperation()):
    with osOperation.open(filePrerequisite.path, "w") as f:
        f.write(filePrerequisite.content)
