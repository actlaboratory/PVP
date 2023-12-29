import re
import wx
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
import simpleDialog

validPatterns = [
	re.compile(r"^\d{1,2}$"),
	re.compile(r"^\d{1,2}:\d{1,2}$"),
	re.compile(r"^\d{1,2}:\d{1,2}:\d{1,2}$"),
	re.compile(r"^\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}$"),
]

class DurationInputDialog(BaseDialog):
	def __init__(self, parent=None, defaultValue=""):
		super().__init__("DurationInputDialog")
		self.title= _("指定時間へ移動")
		self.detail = "h または hh:mm または hh:mm:ss または hh:mm:ss:xxx"
		self.default=defaultValue
		if parent!=None:
			self.parent=parent
		else:
			self.parent=self.app.hMainView.hFrame

	def Initialize(self):
		super().Initialize(self.parent,self.title)
		self.InstallControls()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.VERTICAL,20,style=wx.ALL|wx.EXPAND,margin=20)
		self.edit,self.static=self.creator.inputbox(self.detail,defaultValue=self.default,x=-1,style=DEFAULT_STYLE|self.style,sizerFlag=wx.EXPAND)
		self.edit.hideScrollBar(wx.HORIZONTAL)

		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.HORIZONTAL,20,style=wx.ALIGN_RIGHT)
		self.bOk=self.creator.okbutton(_("ＯＫ"),self.ok)
		self.bCancel=self.creator.cancelbutton(_("キャンセル"),None)

	def ok(self,event):
		if not self.validate():
			return
		event.Skip()

	def GetData(self):
		return self.edit.GetValue()

	def validate(self):
		val = self.edit.GetValue()
		found = False
		for pattern in validPatterns:
			if pattern.match(val):
				found = True
				break
		if found:
			return True
		# end パターンマッチ
		simpleDialog.errorDialog(_("入力された内容を時間として読み取れませんでした。"), self.wnd)
