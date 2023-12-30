# -*- coding: utf-8 -*-
#View Creator
#Copyright (C) 2019-2020 yamahubuki <itiro.ishino@gmail.com>
#Copyright (C) 2019-2020 Hiroki Fujii <hfujii@hisystron.com>

import wx
import wx.media
import win32api
import _winxptheme

from views import ViewCreatorBase
from views.ViewCreatorBase import *
from views.viewObjects import MediaCtrlBase

class ViewCreator(ViewCreatorBase):
	def __init__(self, *pArg, **kArg):
		"""
		ViewCreator

		:param str mode: Set view mode.
		:param wx.Window parent: Set parent window.
		:param wx.Sizer parentSizer: Set parent sizer. Default is None.
		:param flag orient: Set Set widget layout. Default is wx.HORIZONTAL.
		:param int space: Set gap between items. Default is 0.
		:param str/int label: Set item label(str) or grid sizer's column count(int).
		:param flags style: Set sizer flags.
		:param int proportion: Set proportion.
		:param int margin: Set viewCreator's margin.
		"""

		super().__init__(*pArg, **kArg)

		# 標準オブジェクトの変更が必要ならば記述
		# self.winObject["object_name"] = newObject

	def mediaCtrl(self,text, event=None, fileName="", style=wx.BORDER_RAISED, size=(-1,-1), sizerFlag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, proportion=0,margin=5, textLayout=wx.DEFAULT, enableTabFocus=True):
		hStaticText,sizer,parent=self._addDescriptionText(text, textLayout, sizerFlag, proportion, margin)

		ctrl=MediaCtrlBase.MediaCtrl(parent, wx.ID_ANY,size=size,name=text,fileName=fileName,style=style | wx.BORDER_RAISED, enableTabFocus=enableTabFocus)
		ctrl.Bind(wx.media.EVT_MEDIA_STATECHANGED,event)
		self._setFace(ctrl)
		Add(sizer,ctrl,proportion,sizerFlag,margin)
		self.AddSpace()
		return ctrl,hStaticText
