import wx

class NewTextEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)

        self.msg = ''

    def setText(self, text):
        self.msg = text

    def getText(self):
        return self.msg
