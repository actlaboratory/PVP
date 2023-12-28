import os

# defines temp dir structure

tempdirStructure = {
    "temp": {
        "logs": {},
        "concats": {},
    },
}


def tempdirRoot():
    return os.path.join(os.getcwd(), list(tempdirStructure.keys())[0])
