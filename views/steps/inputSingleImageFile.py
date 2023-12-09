import wx
import domain
from .tabPanelBase import *


class InputSingleImageFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("画像ファイル"), x = 300)
		self.browseButton = self.creator.button(_("参照"), event=self.onBrowseButtonClick)

	def onBrowseButtonClick(self, event):
		extensions = ";".join(["*." + x for x in domain.supportedImageFileTypes])
		with wx.FileDialog(
			self.hPanel,
			_("画像ファイルを選択"),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
			wildcard=_("音声ファイル") + "|" + extensions
		) as dlg:
			if dlg.ShowModal() != wx.ID_CANCEL:
				self.fileNameInput.SetValue(dlg.GetPath())

def getValueOrNone(self):
	"""入力値: strまたはNone"""
	if self.fileNameInput.GetValue() == "":
		return None
	return self.fileNameInput.GetValue()
