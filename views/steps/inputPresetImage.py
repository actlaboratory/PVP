import wx
import domain
from .tabPanelBase import *


class InputPresetImage(TabPanelBase):
	def InstallControls(self):
		self.choices = [_("未選択")]
		self.choices.extend([x.displayName for x in domain.availablePresetImages])
		self.presetSelection, unused = self.creator.listbox(_("プリセット画像から選択"), choices=self.choices)
		self.presetSelection.SetSelection(0)
