import wx
from .tabPanelBase import *
import domain


class OutputSingleVideoFile(TabPanelBase):
	def InstallControls(self):
		fileInputArea = views.ViewCreator.ViewCreator(self.creator.GetMode(),self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL | wx.EXPAND,margin=0)
		self.fileNameInput, unused = fileInputArea.inputbox(_("映像ファイルの保存先"), x = 500, proportion=1, textLayout=wx.VERTICAL, margin=0)
		self.fileNameInput.hideScrollBar(wx.HORIZONTAL)
		self.browseButton = fileInputArea.button(_("参照"), event=self.onBrowseButtonClick,sizerFlag=wx.ALIGN_BOTTOM | wx.BOTTOM, margin=3)

	def onBrowseButtonClick(self, event):
		extensions = ";".join(["*." + x for x in domain.supportedVideoFileTypes])
		with wx.FileDialog(
			self.hPanel,
			_("映像ファイルの保存先を選択"),
			style=wx.FD_SAVE,
			wildcard=_("映像ファイル") + "|" + extensions
		) as dlg:
			if dlg.ShowModal() != wx.ID_CANCEL:
				self.fileNameInput.SetValue(dlg.GetPath())

	def getValueOrNone(self):
		"""入力値: strまたはNone"""
		if self.fileNameInput.GetValue() == "":
			return None
		return self.fileNameInput.GetValue()
