# -*- coding: utf-8 -*-

import datetime
import wx
import globalVars
import views.ViewCreator
from views.baseDialog import *
import constants
import adapter
import domain


class ProcessingDialog(BaseDialog):
	def __init__(self, task):
		self.identifier="processingDialog"
		super().__init__(self.identifier)
		self.task = task
		self.result = None

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame, _("実行しています..."))
		self.InstallControls()
		chain = domain.generateFfmpegCommand(self.task)
		now = datetime.datetime.now()
		self.runner = adapter.runCmdChainInBackground(chain, now, self.onEachCmdFinished, self.onEntireTaskFinished)
		self.log.debug("command chain started in background: %s" % self.runner)
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20, style=wx.EXPAND, margin=20)
		self.cancelButton = self.creator.cancelbutton(_("中止"), event=self.onCancelButtonClick)

	def onEachCmdFinished(self, result):
		# これの実行主体は別スレッドなので、メインスレッドに処理を委譲する
		wx.CallAfter(self._onEachCmdFinished, result)

	def _onEachCmdFinished(self, result):
		self.log.debug("command runner %s finished" % (result.identifier))
		self.log.debug("---- logFilePath ----")
		self.log.debug(result.logFilePath)
		self.log.debug("---- returncode ----")
		self.log.debug(result.returncode)
		self.log.debug("---- exception ----")
		self.log.debug(result.exception)
		self.log.debug("---- end of result ----")

	def onEntireTaskFinished(self, result):
		wx.CallAfter(self._onEntireTaskFinished, result)

	def _onEntireTaskFinished(self, result):
		self.log.debug("chain execution finished")
		self.result = result
		self.wnd.EndModal(wx.ID_OK)

	def getValue(self):
		return self.result

	def onCancelButtonClick(self, event):
		self.log.debug("cancel button clicked")
		self.runner.cancel()
		self.runner.join()
		self.wnd.EndModal(wx.ID_CANCEL)
