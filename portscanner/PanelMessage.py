import wx


from NewTextEvent import NewTextEvent
          
TextEventType = wx.NewEventType()
EVT_THREAD_TEXT_EVENT = wx.PyEventBinder(TextEventType, 1)


class PanelMessage(object):
	def __init__(self, window):
		self.window = window
		
	def send(self, message):	
		evt1 = NewTextEvent(TextEventType, -1)
		evt1.setText(message)
		wx.PostEvent(self.window, evt1)
