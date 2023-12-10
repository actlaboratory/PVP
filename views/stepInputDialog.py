# -*- coding: utf-8 -*-
# Step inputs dialog

import wx
import globalVars
import views.ViewCreator
import views.steps as steps
from logging import getLogger
from views.baseDialog import *
from views.stepConfirmDialog import StepConfirmDialog
import constants


panelMap = {
	"InputSingleAudioFile": steps.InputSingleAudioFile,
	"InputPresetImage": steps.InputPresetImage,
	"InputSingleImageFile": steps.InputSingleImageFile,
	"OutputTweetableVideoFile": steps.OutputTweetableVideoFile,
}

class StepInputDialog(BaseDialog):
	def __init__(self, task):
		self.identifier="stepInputDialog"
		super().__init__(self.identifier)

		self.task = task
		self.currentStage = 0
		self.totalStages = task.numberOfSteps()
		self.stepPanels = []

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame, _("入力"))
		self.InstallControls()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20, style=wx.EXPAND, margin=20)
		self.tabCtrl = self.creator.tabCtrl(_("ステップ"), self.onTabChanged, style=wx.NB_NOPAGETHEME|wx.NB_MULTILINE, proportion=1, sizerFlag=wx.EXPAND)
		self.tabCtrl.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.beforeTabChange)

		pageSelectButtonArea = views.ViewCreator.ViewCreator(self.viewMode, self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALL, margin=20)
		self.next = pageSelectButtonArea.button(_("次のステップ"), event=self.onNextButtonClick)
		self.back = pageSelectButtonArea.button(_("前のステップ"), event=self.onBackButtonClick)

		bottomButtonArea = views.ViewCreator.ViewCreator(self.viewMode, self.creator.GetPanel(), self.creator.GetSizer(), wx.HORIZONTAL, 20, style=wx.ALIGN_RIGHT, margin=20)
		self.abort = bottomButtonArea.cancelbutton(_("中止"))

		self.setupTabs()
		self.toNextStage()
		self.updateButtonAttributes()

	def nthPanel(self, n):
		"""指定されたステージのパネルを返す。"""
		return self.stepPanels[n - 1]

	def beforeTabChange(self, event):
		"""タブが変更される前の処理。変更前のステップの入力値を保存したりバリデーションしたりする。"""
		if self.currentStage == 0:
			return
		# end まだステップが選択されていない
		panel = self.nthPanel(self.currentStage)
		step = self.task.nthStep(self.currentStage)
		val = panel.getValueOrNone()
		if val is None:
			step.clearValue()
			return
		# end 入力されていない or クリア
		result = step.tryToSetValue(val)
		if result is True:
			return
		# end バリデーションOK
		if result.allowForce is not True:
			dlg = wx.MessageDialog(self.wnd, "ステップの入力値が不正です。内容を確認して、設定しなおしてください。" + "\n" + result.message, _("エラー"), wx.OK | wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()
			event.Veto()
			return
		# end バリデーションNG
		# バリデーションNGだが、強制的に設定することが許可されている
		# 例えば、ファイルの上書きなど
		dlg = StepConfirmDialog(self.wnd, result.message + "\n" + _("本当にこの設定値で続行しますか？"))
		if dlg.ShowModal() == wx.ID_YES:
			step.tryToSetValue(val, force = True)
			return
		# end 強制
		event.Veto()

	def onTabChanged(self, event):
		"""タブが変更されたあとの処理。currentStageへの反映"""
		self.currentStage = event.GetSelection() + 1
		self.updateButtonAttributes()

	def toNextStage(self):
		"""次のステージに進む。"""
		if self.currentStage > self.totalStages:
			self.Destroy()
			return
		# end 終了
		self.currentStage += 1
		self.tabCtrl.SetSelection(self.currentStage - 1)

	def toPreviousStage(self):
		"""前のステージに戻る。"""
		if self.currentStage == 1:
			self.Destroy()
			return
		# end 終了
		self.currentStage -= 1
		self.tabCtrl.SetSelection(self.currentStage - 1)

	def setupTabs(self):
		"""必要なステップのタブを追加する。"""
		for i in range(1, self.totalStages + 1):
			step = self.task.nthStep(i)
			self.addTab(i, step)

	def addTab(self, stage, step):
		"""指定されたステージのタブを追加する。"""
		requirement = _("必須") if step.isRequired() else _("任意")
		name = "%d/%d %s (%s)" % (stage, self.totalStages, step.stepDescription(), requirement)
		vc = views.ViewCreator.ViewCreator(self.viewMode, self.tabCtrl, None, wx.VERTICAL, 20, name, style=wx.EXPAND|wx.ALL, proportion=1)
		panelClass = panelMap[step.stepType()]
		panel = panelClass(vc, step, stage, self.totalStages)
		self.stepPanels.append(panel)

	def updateButtonAttributes(self):
		"""現在のステージに応じて、ボタンのラベルや活性状態を変更する。"""
		if self.currentStage == self.totalStages:
			self.next.SetLabel(_("完了"))
		else:
			self.next.SetLabel(_("次のステップ"))
		if self.currentStage == 1:
			self.back.Disable()
		else:
			self.back.Enable()

	def onNextButtonClick(self, event):
		if self.currentStage == self.totalStages:
			return
		# end 最後のステップ
		self.toNextStage()
		self.updateButtonAttributes()

	def onBackButtonClick(self, event):
		if self.currentStage == 1:
			return
		# end 最初のステップ
		self.toPreviousStage()
		self.updateButtonAttributes()

	def Destroy(self, events = None):
		self.log.debug("destroy")
		self.wnd.Destroy()
