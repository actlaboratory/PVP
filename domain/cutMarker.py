"""
Cut markers are used to determine the cut points of a video.
"""


class TimePoint:
    def __init__(self, hour, minute, second, millisecond):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond


class CutMarker:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint

