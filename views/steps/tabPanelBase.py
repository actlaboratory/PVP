import wx
import _winxptheme
import globalVars
import views.ViewCreator


class TabPanelBase():
	def __init__(self, vc, step, stage, totalStages):
		self.step = step
		self.hPanel=vc.GetPanel()
		self.creator = vc
		self.InstallControls()

	def InstallControls(self):
		pass

	def getValueOrNone(self):
		"""入力値を取得して返す。入力されていない場合はNoneを返す。"""
		raise NotImplementedError("you must implement getValueOrNone method")
