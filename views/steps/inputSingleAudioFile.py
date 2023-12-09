import wx
import domain
from .tabPanelBase import *


class InputSingleAudioFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("音声ファイル"), x = 300)
		self.browseButton = self.creator.button(_("参照"), event=self.onBrowseButtonClick)

	def onBrowseButtonClick(self, event):
		extensions = ";".join(["*." + x for x in domain.supportedAudioFileTypes])
		with wx.FileDialog(
			self.hPanel,
			_("音声ファイルを選択"),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
			wildcard=_("音声ファイル") + "|" + extensions
		) as dlg:
			if dlg.ShowModal() != wx.ID_CANCEL:
				self.fileNameInput.SetValue(dlg.GetPath())