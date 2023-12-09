import wx
from .tabPanelBase import *


class InputSingleAudioFile(TabPanelBase):
	def InstallControls(self):
		self.fileNameInput, unused = self.creator.inputbox(_("音声ファイル"), x = 300)
		self.browseButton = self.creator.button(_("参照"))
