import wx
from .tabPanelBase import *


class InputSingleAudioFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("オーディオファイル"), x = 300)
		self.browseButton = self.creator.button(_("参照"))
