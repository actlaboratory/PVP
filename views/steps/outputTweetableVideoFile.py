import wx
from .tabPanelBase import *


class OutputTweetableVideoFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("映像ファイルの保存先"), x = 300)
		self.browseButton = self.creator.button(_("参照"))
