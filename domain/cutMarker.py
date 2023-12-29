"""
Cut markers are used to determine the cut points of a video.
"""


class CutMarker:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint

