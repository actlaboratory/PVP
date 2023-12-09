import wx
from .tabPanelBase import *


class InputSingleImageFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("画像ファイル"), x = 300)
		self.browseButton = self.creator.button(_("参照"))
