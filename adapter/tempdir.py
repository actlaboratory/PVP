"""
Makes a temporary directory based on the given structure dictionary.
"""

import os
from .os import OSOperation

def makeTempdir(structure, prevDirs=[], osOperation=OSOperation()):
    if len(structure) == 0:
        return
    # end empty
    for k, v in structure.items():
        path = os.path.join(*prevDirs, k)
        if not osOperation.directoryExists(path):
            osOperation.mkdir(path)
        # end make dir
        makeTempdir(v, prevDirs + [k], osOperation)
    # end for
# end makeTempdir
