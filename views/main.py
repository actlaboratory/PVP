﻿# -*- coding: utf-8 -*-
# main view
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
# Copyright (C) 2019-2021 yamahubuki <itiro.ishino@gmail.com>

import wx

import constants
import globalVars
import update
import menuItemsStore

from .base import *
from simpleDialog import *

from views import globalKeyConfig, settingsDialog, versionDialog, stepInputDialog, processingDialog

import adapter
import domain

class MainView(BaseView):
	def __init__(self):
		super().__init__("mainView")
		self.log.debug("created")
		self.events = Events(self, self.identifier)
		title = constants.APP_NAME
		super().Initialize(
			title,
			self.app.config.getint(self.identifier, "sizeX", 800, 400),
			self.app.config.getint(self.identifier, "sizeY", 600, 300),
			self.app.config.getint(self.identifier, "positionX", 50, 0),
			self.app.config.getint(self.identifier, "positionY", 50, 0)
		)
		self.InstallMenuEvent(Menu(self.identifier), self.events.OnMenuSelect)
		self.InstallControls()


	def InstallControls(self):
		vc = self.creator
		self.whatToDo, unused = vc.listCtrl(_("今日は何をしますか？"), proportion=1, sizerFlag=wx.EXPAND)
		self.whatToDo.AppendColumn(_("タスク"), width = 450)
		self.whatToDo.AppendColumn(_("説明"), width = 1000)
		self.whatToDo.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.events.startTask)
		for task in domain.supportedTasks():
			self.whatToDo.Append([task.displayName, task.description])
		# end append task

		buttonArea = views.ViewCreator.ViewCreator(self.viewMode, vc.GetPanel(), vc.GetSizer(), wx.HORIZONTAL, style=wx.ALIGN_RIGHT)
		self.ok = buttonArea.okbutton(_("開始"), self.events.startTask)
		self.exit = buttonArea.cancelbutton(_("終了"), event = self.events.exit)


class Menu(BaseMenu):
	def Apply(self, target):
		"""指定されたウィンドウに、メニューを適用する。"""

		# メニュー内容をいったんクリア
		self.hMenuBar = wx.MenuBar()

		# メニューの大項目を作る
		self.hFileMenu = wx.Menu()
		self.hOptionMenu = wx.Menu()
		self.hHelpMenu = wx.Menu()

		# ファイルメニュー
		self.RegisterMenuCommand(self.hFileMenu, {
			"FILE_EXIT": self.parent.events.exit,
		})

		# オプションメニュー
		self.RegisterMenuCommand(self.hOptionMenu, {
			"OPTION_OPTION": self.parent.events.option,
			"OPTION_KEY_CONFIG": self.parent.events.keyConfig,
		})

		# ヘルプメニュー
		self.RegisterMenuCommand(self.hHelpMenu, {
			"HELP_UPDATE": self.parent.events.checkUpdate,
			"HELP_VERSIONINFO": self.parent.events.version,
		})

		# メニューバーの生成
		self.hMenuBar.Append(self.hFileMenu, _("ファイル(&F))"))
		self.hMenuBar.Append(self.hOptionMenu, _("オプション(&O)"))
		self.hMenuBar.Append(self.hHelpMenu, _("ヘルプ(&H)"))
		target.SetMenuBar(self.hMenuBar)


class Events(BaseEvents):
	def __init__(self, parent, identifier):
		super().__init__(parent, identifier)
		self.didSomething = False

	def exit(self, event):
		if self.didSomething:
			with wx.MessageDialog(self.parent.hFrame, _("作業フォルダの中身をきれいにしてから終了しますか？"), _("確認"), wx.YES_NO | wx.ICON_QUESTION) as d:
				if d.ShowModal() == wx.ID_YES:
					adapter.cleanTempdir()
				# end if
			# end with
		# end 何かした
		self.parent.hFrame.Close()

	def option(self, event):
		d = settingsDialog.Dialog()
		d.Initialize()
		d.Show()

	def keyConfig(self, event):
		if self.setKeymap(self.parent.identifier, _("ショートカットキーの設定"), filter=keymap.KeyFilter().SetDefault(False, False)):
			# ショートカットキーの変更適用とメニューバーの再描画
			self.parent.menu.InitShortcut()
			self.parent.menu.ApplyShortcut(self.parent.hFrame)
			self.parent.menu.Apply(self.parent.hFrame)

	def checkUpdate(self, event):
		update.checkUpdate()

	def version(self, event):
		d = versionDialog.dialog()
		d.Initialize()
		r = d.Show()

	def setKeymap(self, identifier, ttl, keymap=None, filter=None):
		if keymap:
			try:
				keys = keymap.map[identifier.upper()]
			except KeyError:
				keys = {}
		else:
			try:
				keys = self.parent.menu.keymap.map[identifier.upper()]
			except KeyError:
				keys = {}
		keyData = {}
		menuData = {}
		for refName in defaultKeymap.defaultKeymap[identifier].keys():
			title = menuItemsDic.getValueString(refName)
			if refName in keys:
				keyData[title] = keys[refName]
			else:
				keyData[title] = _("なし")
			menuData[title] = refName

		d = globalKeyConfig.Dialog(keyData, menuData, [], filter)
		d.Initialize(ttl)
		if d.Show() == wx.ID_CANCEL:
			return False

		keyData, menuData = d.GetValue()

		# キーマップの既存設定を置き換える
		newMap = ConfigManager.ConfigManager()
		newMap.read(constants.KEYMAP_FILE_NAME)
		for name, key in keyData.items():
			if key != _("なし"):
				newMap[identifier.upper()][menuData[name]] = key
			else:
				newMap[identifier.upper()][menuData[name]] = ""
		newMap.write()
		return True

	def startTask(self, event):
		selected = self.parent.whatToDo.GetFirstSelected()
		if selected == -1:
			return
		# end if
		taskDef = domain.supportedTasks()[selected]
		task = taskDef.generateNewTask()
		d = stepInputDialog.StepInputDialog(task)
		d.Initialize()
		d.Show()
		if task.isCanceled():
			return
		# end キャンセル
		self.didSomething = True
		prereq = task.getPrerequisites()
		for p in prereq:
			# 今はFilePrerequisiteしかない
			adapter.createFilePrerequisite(p)
		# end for
		d = processingDialog.ProcessingDialog(task)
		d.Initialize()
		code = d.Show()
		if code == wx.ID_OK:
			self.showFinishDialog(d.getValue())
		else:
			self.showCancelDialog()
		# end if
		d.Destroy()

	def showFinishDialog(self, result):
		if len(result.failures) == 0:
			dialog(_("完了"), _("コマンドの実行が完了しました。"))
			return
		# end 成功
		# TODO: とりあえず1つだけ表示している
		lastResult = result.failures[0]
		if lastResult.exception:
			dialog(_("エラー"), _("コマンドの実行中に予期せぬエラーが発生しました。") + "\n" + str(result.exception))
			return
		# end エラー
		if lastResult.returncode != 0:
			dialog(_("エラー"), _("コマンドを実行した結果、エラーが返されました。エラーログを開発者に送ってみてください。"))
			return
		# end エラー

	def showCancelDialog(self):
		dialog(_("キャンセル"), _("コマンドの実行をキャンセルしました。"))
