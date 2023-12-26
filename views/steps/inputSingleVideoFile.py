import wx
import domain
import views
from .tabPanelBase import *


class InputSingleVideoFile(TabPanelBase):
	def InstallControls(self):
		fileInputArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.fileNameInput, unused = fileInputArea.inputbox(_("動画ファイル"), x = 500, proportion=1, textLayout=wx.VERTICAL, margin=0)
		self.fileNameInput.hideScrollBar(wx.HORIZONTAL)
		self.browseButton = fileInputArea.button(_("参照"), event=self.onBrowseButtonClick,sizerFlag=wx.ALIGN_BOTTOM | wx.BOTTOM, margin=3)

	def onBrowseButtonClick(self, event):
		extensions = ";".join(["*." + x for x in domain.supportedVideoFileTypes])
		with wx.FileDialog(
			self.hPanel,
			_("動画ファイルを選択"),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
			wildcard=_("動画ファイル") + "|" + extensions
		) as dlg:
			if dlg.ShowModal() != wx.ID_CANCEL:
				self.fileNameInput.SetValue(dlg.GetPath())

	def getValueOrNone(self):
		"""入力値: strまたはNone"""
		if self.fileNameInput.GetValue() == "":
			return None
		return self.fileNameInput.GetValue()
