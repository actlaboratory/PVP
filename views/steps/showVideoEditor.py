import wx
import wx.media
import domain
from .tabPanelBase import *


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

class ShowVideoEditor(TabPanelBase):
	def InstallControls(self):
		self._cutMarkerList = []
		self._seekInterval = SeekInterval("percent", 1)
		self._lastStartPoint = None
		self._lastEndPoint = None
		self._lastLoadedFile = None
		self.installIntervalMenu()
		self.mediaCtrl = wx.media.MediaCtrl(self.hPanel, name=_("メディアコントロール"))
		self.mediaCtrl.Bind(wx.media.EVT_MEDIA_STATECHANGED, self.onMediaStateChange)
		buttonsArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.playButton = buttonsArea.button(_("再生"), self.onPlayButtonClick)
		self.backwardButton = buttonsArea.button(_("%(interval)s戻す") % {"interval": self._seekInterval}, self.onBackwardButtonClick)
		self.forwardButton = buttonsArea.button(_("%(interval)s進める") % {"interval": self._seekInterval}, self.onForwardButtonClick)
		self.changeIntervalButton = buttonsArea.button(_("間隔調整: %(interval)s") % {"interval": self._seekInterval}, self.onChangeIntervalPopup)
		self.gotoButton = buttonsArea.button(_("指定時間へ"))
		self.cutTriggerButton = buttonsArea.button(_("ここからカット"))
		listArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.markersListCtrl, unused = listArea.listbox(_("カットする箇所"), style=wx.LB_SINGLE, size=(200, 300))
		self.updateButtons()

	def installIntervalMenu(self):
		self.intervalMenuMap = {
			1001: SeekInterval("second", 3),
			1002: SeekInterval("second", 5),
			1003: SeekInterval("second", 10),
			1004: SeekInterval("second", 30),
			1005: SeekInterval("second", 60),
			1006: SeekInterval("second", 180),
			1007: SeekInterval("second", 300),
			1008: SeekInterval("second", 600),
			1009: SeekInterval("percent", 1),
			1010: SeekInterval("percent", 5),
			1011: SeekInterval("percent", 10),
		}
		menu = wx.Menu()
		self.item1 = menu.Append(1001, _("3秒"))
		menu.Append(1002, _("5秒"))
		menu.Append(1003, _("10秒"))
		menu.Append(1004, _("30秒"))
		menu.Append(1005, _("1分"))
		menu.Append(1006, _("3分"))
		menu.Append(1007, _("5分"))
		menu.Append(1008, _("10分"))
		menu.Append(1009, _("1%"))
		menu.Append(1010, _("5%"))
		menu.Append(1011, _("10%"))
		menu.Bind(wx.EVT_MENU, self.onChangeInterval)
		self.intervalMenu = menu

	def getValueOrNone(self):
		"""入力値: domain.CutMarker のリスト or None"""
		if len(self._cutMarkerList) == 0:
			return None
		return self._cutMarkerList

	def onChangeIntervalPopup(self, event):
		self.hPanel.PopupMenu(self.intervalMenu)

	def onChangeInterval(self, event):
		self._seekInterval = self.intervalMenuMap[event.GetId()]
		self.updateButtons()

	def onActivated(self):
		f = self.task.getInputFileName()
		if f is None:
			return
		# end ファイルが指定されていない
		if f != self._lastLoadedFile:
			self._cutMarkerList = []
			self._lastStartPoint = None
			self._lastEndPoint = None
			self.markersListCtrl.Clear()
		# end ファイルが変更された
		self.mediaCtrl.Load(f)
		self._lastLoadedFile = f

	def onDeactivated(self):
		if self.mediaCtrl.GetState() == wx.media.MEDIASTATE_PLAYING:
			self.mediaCtrl.Stop()

	def updateButtons(self):
		self.changeIntervalButton.SetLabel(_("間隔調整: %(interval)s") % {"interval": self._seekInterval})
		self.backwardButton.SetLabel(_("%(interval)s戻す") % {"interval": self._seekInterval})
		self.forwardButton.SetLabel(_("%(interval)s進める") % {"interval": self._seekInterval})
		state = self.mediaCtrl.GetState()
		if state == wx.media.MEDIASTATE_PLAYING:
			self.playButton.SetLabel(_("停止"))
		else:
			self.playButton.SetLabel(_("再生"))

	def onMediaStateChange(self, event):
		self.updateButtons()

	def onPlayButtonClick(self, event):
		if self.mediaCtrl.GetState() == wx.media.MEDIASTATE_PLAYING:
			self.mediaCtrl.Pause()
		else:
			self.mediaCtrl.Play()

	def onBackwardButtonClick(self, event):
		length = self.mediaCtrl.Length()
		newpos = self._seekInterval.calcPosition(length) * -1
		self.mediaCtrl.Seek(newpos, wx.FromCurrent)

	def onForwardButtonClick(self, event):
		length = self.mediaCtrl.Length()
		newpos = self._seekInterval.calcPosition(length)
		self.mediaCtrl.Seek(newpos, wx.FromCurrent)
