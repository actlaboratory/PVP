import re

if '_' not in globals():
    globals()['_'] = lambda x: x


class SeekInterval:
    def __init__(self, secondOrPercent, value):
        if secondOrPercent not in ["second", "percent"]:
            raise ValueError("secondOrPercent must be 'second' or 'percent'")
        # end if
        self.secondOrPercent = secondOrPercent
        self.value = value

    def __str__(self):
        if self.secondOrPercent == "second":
            return self._strSecond()
        else:
            return str(self.value) + _("パーセント")

    def _strSecond(self):
        if self.value % 60 == 0:
            return str(self.value // 60) + _("分")
        else:
            return str(self.value) + _("秒")

    def calcPosition(self, length):
        if self.secondOrPercent == "second":
            return self.value * 1000
        else:
            return length * self.value // 100

def millisecondsToPositionStr(milliseconds):
    hour = milliseconds // (60 * 60 * 1000)
    milliseconds -= hour * 60 * 60 * 1000
    minute = milliseconds // (60 * 1000)
    milliseconds -= minute * 60 * 1000
    second = milliseconds // 1000
    milliseconds -= second * 1000
    return "%02d:%02d:%02d.%03d" % (hour, minute, second, milliseconds)

def positionStrToMilliseconds(positionStr):
    match = re.match(r"(\d+):(\d+):(\d+)\.(\d+)", positionStr)
    if match is None:
        raise ValueError("Invalid position string: " + positionStr)
    # end if
    hour = int(match.group(1))
    minute = int(match.group(2))
    second = int(match.group(3))
    millisecond = int(match.group(4))
    return (hour * 60 * 60 + minute * 60 + second) * 1000 + millisecond

def normalizeToFullPositionStr(positionStr):
    m1 = re.match(r"^(\d+)$", positionStr)
    if m1 is not None:
        return millisecondsToPositionStr(int(m1.group(1)) * 1000 * 60)
    # end if
    m2 = re.match(r"^(\d+):(\d+)$", positionStr)
    if m2 is not None:
        return millisecondsToPositionStr(int(m2.group(1)) * 1000 * 60 + int(m2.group(2)) * 1000)
    # end if
    m3 = re.match(r"^(\d+):(\d+):(\d+)$", positionStr)
    if m3 is not None:
        return millisecondsToPositionStr(int(m3.group(1)) * 1000 * 60 * 60 + int(m3.group(2)) * 1000 * 60 + int(m3.group(3)) * 1000)
    # end if
    return positionStr
