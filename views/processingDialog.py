# -*- coding: utf-8 -*-

import wx
import globalVars
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
import constants


class ProcessingDialog(BaseDialog):
	def __init__(self):
		self.identifier="processingDialog"
		super().__init__(self.identifier)

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame, _("実行しています..."))
		self.InstallControls()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20, style=wx.EXPAND, margin=20)
		self.cancelButton = self.creator.cancelbutton(_("中止"))

