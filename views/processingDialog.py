# -*- coding: utf-8 -*-

import datetime
import wx
import globalVars
import views.ViewCreator
from logging import getLogger
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
		cmd = domain.generateFfmpegCommand(self.task)
		self.log.debug("Preparing to run command: %s" % " ".join(cmd))
		now = datetime.datetime.now()
		self.runner = adapter.runCmdInBackground(cmd, now, onFinished = self.onCommandFinish)
		self.log.debug("command started in background")
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20, style=wx.EXPAND, margin=20)
		self.cancelButton = self.creator.cancelbutton(_("中止"), event=self.onCancelButtonClick)

	def onCommandFinish(self, result):
		# これの実行主体は別スレッドなので、メインスレッドに処理を委譲する
		wx.CallAfter(self._onCommandFinish, result)

	def _onCommandFinish(self, result):
		self.result = result
		self.log.debug("command finished")
		self.log.debug("---- logFilePath ----")
		self.log.debug(result.logFilePath)
		self.log.debug("---- returncode ----")
		self.log.debug(result.returncode)
		self.log.debug("---- exception ----")
		self.log.debug(result.exception)
		self.log.debug("---- end of result ----")
		self.runner.join()
		self.wnd.EndModal(wx.ID_OK)

	def getValue(self):
		return self.result

	def onCancelButtonClick(self, event):
		self.log.debug("cancel button clicked")
		self.runner.cancel()
		self.runner.join()
		self.wnd.EndModal(wx.ID_CANCEL)
