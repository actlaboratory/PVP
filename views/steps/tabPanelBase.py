import wx
import _winxptheme
import globalVars
import views.ViewCreator


class TabPanelBase():
	def __init__(self, parentNotebook, step, stage, totalStages):
		self.step = step
		self.hPanel=views.ViewCreator.makePanel(parentNotebook)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.hPanel.SetSizer(self.sizer)
		self.viewMode=views.ViewCreator.ViewCreator.config2modeValue(
			globalVars.app.config.getstring("view","colorMode","white",("white","dark")),
			globalVars.app.config.getstring("view","textWrapping","off",("on","off"))
		)
		self.creator = views.ViewCreator.ViewCreator(self.viewMode, self.hPanel, self.sizer, wx.VERTICAL, 20)
		self.InstallControls()

	def InstallControls(self):
		pass

	def getValueOrNone(self):
		"""入力値を取得して返す。入力されていない場合はNoneを返す。"""
		print("base")
