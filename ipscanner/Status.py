import wx
from NewIntEvent import NewIntEvent

gaugeEventType = wx.NewEventType()
EVT_GAUGE_EVENT = wx.PyEventBinder(gaugeEventType, 1)

class Status(object):
	def __init__(self, total, window):
		#get gauage instance from scanner
		self.output_window = window
				
		self.count = 0.0
		self.total = total
		
	def add(self):
		#increase the task count
		self.count = self.count + 1
		
		#calculate the percentage done using the given end count
		fraction = self.count / self.total
		percent = int(round(fraction * 100, 0))		
		
		#set a calss field for the progress bar to use
		self.progress = percent
		
		#pass progress bar count through gauge event
		evt = NewIntEvent(gaugeEventType, -1)
		evt.setValue(percent)
		wx.PostEvent(self.output_window, evt)
		
	def reset(self):
		evt = NewIntEvent(gaugeEventType, -1)
		evt.setValue(0)
		wx.PostEvent(self.output_window, evt)
		
