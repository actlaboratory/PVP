"""
Cut markers are used to determine the cut points of a video.
CutMarker has start and end points, and they are expressed as a position string like "00:00:00.000".
"""


class CutMarker:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint

    def pointsFileTop(self):
        return self.startPoint == "00:00:00.000"
