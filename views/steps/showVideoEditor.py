import wx
import wx.media
import domain
from .tabPanelBase import *
from .durationInput import DurationInputDialog


class ShowVideoEditor(TabPanelBase):
	def InstallControls(self):
		self._cutMarkerList = []
		self._seekInterval = domain.SeekInterval("percent", 1)
		self._lastStartPoint = None
		self._lastEndPoint = None
		self._lastLoadedFile = None
		self.installIntervalMenu()

		horizontalCreator = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,proportion=1, margin=0)
		leftArea = views.ViewCreator.ViewCreator(horizontalCreator.GetMode(),horizontalCreator.GetPanel(), horizontalCreator.GetSizer(), wx.VERTICAL, 20, style=wx.ALL | wx.EXPAND,margin=0)

		self.mediaCtrl, unused = leftArea.mediaCtrl(_("メディアコントロール"), self.onMediaStateChange, size=(300,300), sizerFlag=wx.EXPAND|wx.ALL, proportion=1, textLayout=None)

		self.markersListCtrl, unused = leftArea.listbox(_("カットする箇所"), style=wx.LB_SINGLE, size=(500, 150))
		self.installContextMenu()
		self.markersListCtrl.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)
		self.markersListCtrl.Bind(wx.EVT_KEY_UP, self.onMarkersListKeyUp)


		buttonsArea = views.ViewCreator.ViewCreator(horizontalCreator.GetMode(), horizontalCreator.GetPanel(), horizontalCreator.GetSizer(), wx.VERTICAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.playButton = buttonsArea.button(_("再生"), self.onPlayButtonClick, sizerFlag=wx.EXPAND)
		self.backwardButton = buttonsArea.button(_("%(interval)s戻す") % {"interval": self._seekInterval}, self.onBackwardButtonClick, sizerFlag=wx.EXPAND)
		self.forwardButton = buttonsArea.button(_("%(interval)s進める") % {"interval": self._seekInterval}, self.onForwardButtonClick, sizerFlag=wx.EXPAND)
		self.changeIntervalButton = buttonsArea.button(_("間隔調整: %(interval)s") % {"interval": self._seekInterval}, self.onChangeIntervalPopup, sizerFlag=wx.EXPAND)
		self.gotoButton = buttonsArea.button(_("指定時間へ"), self.onGotoButtonClick, sizerFlag=wx.EXPAND)
		self.cutTriggerButton = buttonsArea.button(_("ここからカット"), self.onCutTriggerButtonClick, sizerFlag=wx.EXPAND)

		self.installAcceleratorTable()

		self.updateButtons()

	def installIntervalMenu(self):
		self.intervalMenuMap = {
			1001: domain.SeekInterval("second", 3),
			1002: domain.SeekInterval("second", 5),
			1003: domain.SeekInterval("second", 10),
			1004: domain.SeekInterval("second", 30),
			1005: domain.SeekInterval("second", 60),
			1006: domain.SeekInterval("second", 180),
			1007: domain.SeekInterval("second", 300),
			1008: domain.SeekInterval("second", 600),
			1009: domain.SeekInterval("percent", 1),
			1010: domain.SeekInterval("percent", 5),
			1011: domain.SeekInterval("percent", 10),
		}
		menu = wx.Menu()
		menu.Append(1001, _("3秒"))
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

	def installContextMenu(self):
		contextMenu = wx.Menu()
		self.contextMenuDelete = contextMenu.Append(1101, _("削除"))
		self.contextMenuGoToCutStart = contextMenu.Append(1102, _("カット開始地点に移動"))
		self.contextMenuGoToCutEnd = contextMenu.Append(1103, _("カット終了地点に移動"))
		contextMenu.Bind(wx.EVT_MENU, self.onContextMenuSelect)
		self.contextMenu = contextMenu

	def installAcceleratorTable(self):
		acceleratorTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL, ord("P"), self.playButton.GetId()),
			(wx.ACCEL_CTRL, ord("B"), self.backwardButton.GetId()),
			(wx.ACCEL_CTRL, ord("F"), self.forwardButton.GetId()),
			(wx.ACCEL_CTRL, ord("G"), self.gotoButton.GetId()),
			(wx.ACCEL_CTRL, ord("J"), self.cutTriggerButton.GetId()),
			(wx.ACCEL_CTRL, ord("I"), self.changeIntervalButton.GetId()),
		])
		self.hPanel.SetAcceleratorTable(acceleratorTable)

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
		if self._lastStartPoint is None:
			self.cutTriggerButton.SetLabel(_("ここからカット"))
		else:
			self.cutTriggerButton.SetLabel(_("ここまでカット"))
		# ファイルが読み込まれてなければ、全部のボタンを無効化する
		if self._lastLoadedFile is None:
			self.playButton.Enable(False)
			self.backwardButton.Enable(False)
			self.forwardButton.Enable(False)
			self.changeIntervalButton.Enable(False)
			self.gotoButton.Enable(False)
			self.cutTriggerButton.Enable(False)

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

	def onGotoButtonClick(self, event):
		curpos = domain.millisecondsToPositionStr(self.mediaCtrl.Tell())
		dlg = DurationInputDialog(self.hPanel, curpos)
		dlg.Initialize()
		ret = dlg.Show()
		if ret == wx.ID_CANCEL:
			return
		# end cancel
		newpos = domain.positionStrToMilliseconds(domain.normalizeToFullPositionStr(dlg.GetData()))
		self.mediaCtrl.Seek(newpos, wx.FromStart)

	def onCutTriggerButtonClick(self, event):
		if self._lastStartPoint is not None:
			self._lastEndPoint = self.mediaCtrl.Tell()
			self.swapPointsIfNeeded()
			# じつは「ここから」を押した時点で追加しているので、一番最近の要素を更新する
			self._cutMarkerList[-1] = domain.CutMarker(domain.millisecondsToPositionStr(self._lastStartPoint), domain.millisecondsToPositionStr(self._lastEndPoint))
			self._lastStartPoint = None
			self._lastEndPoint = None
			self.updateMarkersList()
			self.updateButtons()
			return
		# end カット終了点
		self._lastStartPoint = self.mediaCtrl.Tell()
		# 開始地点を選んだら、暗黙的に「動画の最後まで」とする
		self._cutMarkerList.append(domain.CutMarker(domain.millisecondsToPositionStr(self._lastStartPoint), None))
		self.updateMarkersList()
		self.updateButtons()

	def swapPointsIfNeeded(self):
		if self._lastStartPoint > self._lastEndPoint:
			tmp = self._lastStartPoint
			self._lastStartPoint = self._lastEndPoint
			self._lastEndPoint = tmp

	def updateMarkersList(self):
		prevIndex = self.markersListCtrl.GetSelection()
		self.markersListCtrl.Clear()
		for m in self._cutMarkerList:
			s = m.startPoint
			e = _("動画の最後") if m.endPoint is None else m.endPoint
			self.markersListCtrl.Append(_("%s から %s まで") % (s, e))
		# end for
		if prevIndex >= 0 and prevIndex < self.markersListCtrl.GetCount():
			self.markersListCtrl.SetSelection(prevIndex)

	def onContextMenu(self, event):
		selectedIndex = self.markersListCtrl.GetSelection()
		if selectedIndex == wx.NOT_FOUND:
			return
		# end 選択されていない
		marker = self._cutMarkerList[selectedIndex]
		if marker.endPoint is None:
			self.contextMenuGoToCutEnd.Enable(False)
		else:
			self.contextMenuGoToCutEnd.Enable(True)
		# end カット終了地点が明示的に設定されているかどうか
		self.hPanel.PopupMenu(self.contextMenu, event.GetPosition())

	def onContextMenuSelect(self, event):
		id = event.GetId()
		if id == 1101:
			self.deleteMarker()
			return
		# end 削除
		if id == 1102:
			self.mediaCtrl.Seek(domain.positionStrToMilliseconds(self._cutMarkerList[self.markersListCtrl.GetSelection()].startPoint), wx.FromStart)
			return
		# end カット開始地点に移動
		if id == 1103:
			self.mediaCtrl.Seek(domain.positionStrToMilliseconds(self._cutMarkerList[self.markersListCtrl.GetSelection()].endPoint), wx.FromStart)
			return
		# end カット終了地点に移動

	def deleteMarker(self):
		index = self.markersListCtrl.GetSelection()
		if index == wx.NOT_FOUND:
			return
		# end 選択されていない
		# 暗黙的に「動画の最後まで」となっているときは、つじつまを合わせる必要がある
		if len(self._cutMarkerList) == index + 1 and self._cutMarkerList[index].endPoint is None:
			self._lastStartPoint = None
		# end つじつま合わせ
		self._cutMarkerList.pop(index)
		self.updateMarkersList()
		self.updateButtons()

	def onMarkersListKeyUp(self, event):
		if event.GetKeyCode() == wx.WXK_DELETE:
			self.deleteMarker()

