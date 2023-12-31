# Media Control
#Copyright (C) 2023 yamahubuki <itiro.ishino@gmail.com>

import wx
import wx.media
from views.viewObjectBase.viewObjectUtil import *
from views.viewObjectBase import viewObjectUtil, controlBase

class MediaCtrl(controlBase.controlBase, wx.media.MediaCtrl):
    def __init__(self, *pArg, **kArg):
        self.focusFromKbd = viewObjectUtil.popArg(kArg, "enableTabFocus", True) #キーボードフォーカスの初期値
        return super().__init__(*pArg, **kArg)
