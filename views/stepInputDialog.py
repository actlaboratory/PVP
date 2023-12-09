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
		self.tabCtrl = self.creator.tabCtrl(_("ステップ"))
		self.next = self.creator.okbutton(_("次のステップ"))
		self.back = self.creator.cancelbutton(_("前のステップ"))
		self.toNextStage()
		self.updateButtonLabels()

	def toNextStage(self):
		"""次のステージに進む。"""
		if self.currentStage > self.totalStages:
			self.Destroy()
			return
		# end 終了
		self.unlockTabs()
		self.currentStage += 1
		self.tabCtrl.SetSelection(self.currentStage - 1)

	def unlockTabs(self):
		"""currentStageの次から調べて、必要なタブをアンロックする。"""
		for i in range(self.currentStage + 1, self.totalStages + 1):
			step = self.task.nthStep(i)
			print("n=%d, step=%s" % (i, step.stepDescription()))
			if i == self.currentStage + 1: # 次のステップはアンロックする
				self.unlockTab(i, step)
				print("unlock")
				# 次のステップが入力必須なら、これより先のステップはアンロックしない
				if step.isRequired():
					break
				# end 次のステップで終わり
			# end 次のステップ
			# 入力が任意のステップはアンロックする
			if not step.isRequired():
				self.unlockTab(i, step)
			else: # 入力必須のステップがあったら止まる
				break

	def unlockTab(self, stage, step):
		"""指定されたステージのタブをアンロックする。"""
		panel = self.makePanel(step, stage)
		self.tabCtrl.AddPage(panel.hPanel, "%d/%d: %s" % (stage, self.totalStages, step.stepDescription()))

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
