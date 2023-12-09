import wx

class StepConfirmDialog(wx.MessageDialog):
	def __init__(self, parent, message):
		super().__init__(parent, message, _("確認"), wx.YES_NO)
		self.SetYesNoLabels(_("問題なし！"), _("戻る"))
