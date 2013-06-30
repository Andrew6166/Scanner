import wx

class NewIntEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)

        self.value = 0

    def setValue(self, integer):
		integer = int(integer)
		self.value = integer

    def getValue(self):
        return self.value
