import wx
import _winxptheme
import globalVars
import views.ViewCreator


class TabPanelBase():
	def __init__(self, vc, task, step, stage, totalStages):
		self.task = task
		self.step = step
		self.hPanel=vc.GetPanel()
		self.creator = vc
		self.InstallControls()

	def InstallControls(self):
		pass

	def getValueOrNone(self):
		"""入力値を取得して返す。入力されていない場合はNoneを返す。"""
		raise NotImplementedError("you must implement getValueOrNone method")

	def onActivated(self):
		pass # タブ選択時に処理を行う場合はオーバーライドする

	def onDeactivated(self):
		pass # タブの選択解除時に処理を行う場合はオーバーライドする
