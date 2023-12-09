# -*- coding: utf-8 -*-
# Step inputs dialog

import wx
import globalVars
import views.ViewCreator
import views.steps as steps
from logging import getLogger
from views.baseDialog import *
import constants


panelMap = {
	"InputSingleAudioFile": steps.InputSingleAudioFile,
	"InputPresetImage": steps.InputPresetImage,
	"InputSingleImageFile": steps.InputSingleImageFile,
	"OutputTweetableVideoFile": steps.OutputTweetableVideoFile,
}

class StepInputDialog(BaseDialog):
	def __init__(self, task):
		#まだglobalVars.appが未精製の状態での軌道の可能性があるのであえて呼ばない
		#super().__init__()
		self.identifier="stepInputDialog"
		self.log=getLogger("%s.%s" % (constants.LOG_PREFIX,self.identifier))
		self.task = task
		self.currentStage = 0
		self.totalStages = task.numberOfSteps()
		self.viewMode="white"

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(None, _("入力"))
		self.InstallControls()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.VERTICAL,20)
		self.tabCtrl = self.creator.tabCtrl(_("ステップ"), self.onTabChanged)
		self.next = self.creator.okbutton(_("次のステップ"))
		self.back = self.creator.cancelbutton(_("前のステップ"))
		self.setupTabs()
		self.toNextStage()
		self.updateButtonLabels()

	def onTabChanged(self, event):
		"""タブが変更されたあとの処理。currentStageへの反映"""
		self.currentStage = event.GetSelection() + 1
		self.updateButtonLabels()

	def toNextStage(self):
		"""次のステージに進む。"""
		if self.currentStage > self.totalStages:
			self.Destroy()
			return
		# end 終了
		self.currentStage += 1
		self.tabCtrl.SetSelection(self.currentStage - 1)

	def setupTabs(self):
		"""必要なステップのタブを追加する。"""
		for i in range(1, self.totalStages + 1):
			step = self.task.nthStep(i)
			self.addTab(i, step)

	def addTab(self, stage, step):
		"""指定されたステージのタブを追加する。"""
		panel = self.makePanel(step, stage)
		requirement = _("必須") if step.isRequired() else _("任意")
		self.tabCtrl.AddPage(panel.hPanel, "%d/%d %s (%s)" % (stage, self.totalStages, step.stepDescription(), requirement))

	def makePanel(self, step, stage):
		"""指定されたステップに対応するパネルを作成する。"""
		panelClass = panelMap[step.stepType()]
		return panelClass(self.tabCtrl, step, stage, self.totalStages)

	def updateButtonLabels(self):
		"""現在のステージに応じて、ボタンのラベルを変更する。"""
		if self.currentStage == self.totalStages:
			self.next.SetLabel(_("完了"))
		else:
			self.next.SetLabel(_("次のステップ"))
		if self.currentStage == 1:
			self.back.SetLabel(_("キャンセル"))
		else:
			self.back.SetLabel(_("前のステップ"))

	def Destroy(self, events = None):
		self.log.debug("destroy")
		self.wnd.Destroy()
