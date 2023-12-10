import wx
import domain
from .tabPanelBase import *


class InputPresetImage(TabPanelBase):
	def InstallControls(self):
		self.choices = [_("未選択")]
		self.choices.extend([x.displayName for x in domain.availablePresetImages])
		self.presetSelection, unused = self.creator.listbox(_("プリセット画像から選択"), choices=self.choices, style=wx.EXPAND)
		self.presetSelection.SetSelection(0)

	def getValueOrNone(self):
		"""入力値: domain.PresetImageまたはNone"""
		if self.presetSelection.GetSelection() == 0:
			return None
		return domain.availablePresetImages[self.presetSelection.GetSelection() - 1]
