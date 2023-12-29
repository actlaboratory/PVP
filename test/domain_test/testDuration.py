import unittest
import domain


class TestSeekInterval(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(domain.SeekInterval("second", 10)), "10秒")
        self.assertEqual(str(domain.SeekInterval("second", 60)), "1分")
        self.assertEqual(str(domain.SeekInterval("second", 61)), "61秒")
        self.assertEqual(str(domain.SeekInterval("percent", 10)), "10パーセント")
        self.assertEqual(str(domain.SeekInterval("percent", 100)), "100パーセント")

    def test_calcPosition(self):
        self.assertEqual(domain.SeekInterval("second", 10).calcPosition(1000), 10000)
        self.assertEqual(domain.SeekInterval("second", 60).calcPosition(1000), 60000)
        self.assertEqual(domain.SeekInterval("percent", 10).calcPosition(1000), 100)
        self.assertEqual(domain.SeekInterval("percent", 100).calcPosition(1000), 1000)

class TestPositionStr(unittest.TestCase):
    def test_millisecondsToPositionStr(self):
        self.assertEqual(domain.millisecondsToPositionStr(0), "00:00:00.000")
        self.assertEqual(domain.millisecondsToPositionStr(1), "00:00:00.001")
        self.assertEqual(domain.millisecondsToPositionStr(10), "00:00:00.010")
        self.assertEqual(domain.millisecondsToPositionStr(100), "00:00:00.100")
        self.assertEqual(domain.millisecondsToPositionStr(1000), "00:00:01.000")
        self.assertEqual(domain.millisecondsToPositionStr(10000), "00:00:10.000")
        self.assertEqual(domain.millisecondsToPositionStr(60000), "00:01:00.000")
        self.assertEqual(domain.millisecondsToPositionStr(61000), "00:01:01.000")
        self.assertEqual(domain.millisecondsToPositionStr(3600000), "01:00:00.000")
        self.assertEqual(domain.millisecondsToPositionStr(3661000), "01:01:01.000")

    def test_positionStrToMilliseconds(self):
        self.assertEqual(domain.positionStrToMilliseconds("00:00:00.000"), 0)
        self.assertEqual(domain.positionStrToMilliseconds("00:00:00.001"), 1)
        self.assertEqual(domain.positionStrToMilliseconds("00:00:00.010"), 10)
        self.assertEqual(domain.positionStrToMilliseconds("00:00:00.100"), 100)
        self.assertEqual(domain.positionStrToMilliseconds("00:00:01.000"), 1000)
        self.assertEqual(domain.positionStrToMilliseconds("00:00:10.000"), 10000)
        self.assertEqual(domain.positionStrToMilliseconds("00:01:00.000"), 60000)
        self.assertEqual(domain.positionStrToMilliseconds("00:01:01.000"), 61000)
        self.assertEqual(domain.positionStrToMilliseconds("01:00:00.000"), 3600000)
        self.assertEqual(domain.positionStrToMilliseconds("01:01:01.000"), 3661000)

    def test_normalizeToFullPositionStr(self):
        self.assertEqual(domain.normalizeToFullPositionStr("0"), "00:00:00.000")
        self.assertEqual(domain.normalizeToFullPositionStr("1"), "00:01:00.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:00:00"), "00:00:00.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:00:01"), "00:00:01.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:00:10"), "00:00:10.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:01:00"), "00:01:00.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:01:01"), "00:01:01.000")
        self.assertEqual(domain.normalizeToFullPositionStr("01:00:00"), "01:00:00.000")
        self.assertEqual(domain.normalizeToFullPositionStr("01:01:01"), "01:01:01.000")
        self.assertEqual(domain.normalizeToFullPositionStr("00:00:00.000"), "00:00:00.000")
