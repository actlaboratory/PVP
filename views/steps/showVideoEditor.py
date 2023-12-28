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
			return str(self.value) + _("秒")
		else:
			return str(self.value) + _("パーセント")


class ShowVideoEditor(TabPanelBase):
	def InstallControls(self):
		self._cutMarkerList = []
		self._seekInterval = SeekInterval("percent", 1)
		self._lastStartPoint = None
		self._lastEndPoint = None
		self.mediaCtrl = wx.media.MediaCtrl(self.hPanel, style=wx.media.MC_NO_AUTORESIZE, name=_("メディアコントロール"))
		buttonsArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.playButton = buttonsArea.button(_("再生"))
		self.backwardButton = buttonsArea.button(_("%(interval)s戻す") % {"interval": self._seekInterval})
		self.forwardButton = buttonsArea.button(_("%(interval)s進める") % {"interval": self._seekInterval})
		self.changeIntervalButton = buttonsArea.button(_("間隔調整: %(interval)s") % {"interval": self._seekInterval})
		self.gotoButton = buttonsArea.button(_("指定時間へ"))
		self.cutTriggerButton = buttonsArea.button(_("ここからカット"))
		listArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.markersListCtrl = listArea.listbox(_("カットする箇所"), style=wx.LB_SINGLE, size=(200, 300))

	def getValueOrNone(self):
		"""入力値: domain.CutMarker のリスト or None"""
		if len(self._cutMarkerList) == 0:
			return None
		return self._cutMarkerList
