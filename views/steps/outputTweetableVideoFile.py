import wx
from .tabPanelBase import *


class OutputTweetableVideoFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("映像ファイルの保存先"), x = 300)
		self.browseButton = self.creator.button(_("参照"), event=self.onBrowseButtonClick)

	def onBrowseButtonClick(self, event):
		with wx.FileDialog(
			self.hPanel,
			_("映像ファイルの保存先を選択"),
			style=wx.FD_SAVE,
			wildcard=_("ツイート可能な映像ファイル") + "(*.mp4)|*.mp4"
		) as dlg:
			if dlg.ShowModal() != wx.ID_CANCEL:
				self.fileNameInput.SetValue(dlg.GetPath())
