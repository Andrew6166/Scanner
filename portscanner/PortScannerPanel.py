import socket
import subprocess
import sys
import Queue
import threading
import time
from ThreadScan import ThreadScan
from PortScanner import PortScan

from PortScanner import TextEventType
from PortScanner import EVT_THREAD_TEXT_EVENT

from PortScanner import StatusEventType
from PortScanner import EVT_STATUS_BAR_EVENT

from Status import gaugeEventType
from Status import EVT_GAUGE_EVENT


import wx


TASK_RANGE = 100




class PortScannerPanel(wx.Panel):
           
	def __init__(self, parent, *args, **kw):
		wx.Panel.__init__(self, parent, size=(600,500),*args, **kw)
                
		self.InitUI()
        
	def InitUI(self):   

		
		
		#sizer
		sizer = wx.GridBagSizer(4, 4)		
	
		#title text
		font1 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		name = wx.StaticText(self, label="Port Scanner")
		name.SetFont(font1)
		sizer.Add(name, pos=(0,2), flag=wx.TOP|wx.BOTTOM, border = 5)
		
		#line
		line = wx.StaticLine(self)
		sizer.Add(line, pos=(1,0), span=(1,8))
		
		#button to start scan
		self.scan_button = wx.ToggleButton(self, label='Scan')
		sizer.Add(self.scan_button, pos=(2,0), flag=wx.LEFT, border=5) 
        
        #label for the host field
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		label = wx.StaticText(self, label='Host:')
		label.SetFont(font)
		sizer.Add(label, pos=(2,1), flag=wx.LEFT, border=20)
		
		#Field for the user to put in the host
		self.text = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.text, pos=(2,2), span=(1,2), flag=wx.EXPAND)
		
        #option to select full scan
		self.check = wx.CheckBox(self, label='Full scan')
		sizer.Add(self.check, pos=(2,4), flag=wx.LEFT, border = 20)
		
		#Label for timeout box
		timeout = wx.StaticText(self, label='Timeout', )
		sizer.Add(timeout, pos=(2,5), flag=wx.LEFT, border = 20)
		
		#Field for timeout
		self.timeout = wx.TextCtrl(self)
		sizer.Add(self.timeout, pos=(2,6), flag=wx.RIGHT|wx.LEFT, border=5)
		
		#initialize with a default value of 2
		self.timeout.SetValue('2')
        
        
        #Field for displaying the output from the scanner, readonly
		self.text_info = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY|wx.TE_AUTO_URL)
		sizer.Add(self.text_info, pos=(3,0), span=(3,8), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)      
        
        #status bar 
		self.gauge = wx.Gauge(self, range=TASK_RANGE)
		sizer.Add(self.gauge, pos=(6,0), span=(1,8), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)       
		
		#set expandable rows and columns		
		sizer.AddGrowableRow(3)
		sizer.AddGrowableCol(7)		
		
		#Exit key bindings
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		
		#bind button to method to call port scanner
		self.scan_button.Bind(wx.EVT_TOGGLEBUTTON, self.Scanner)
		
		#Bind the text box to the enter key
		self.text.Bind(wx.EVT_TEXT_ENTER, self.Scanner)
		
        
        #bind the custom events for updating status bar, text window, gauge to respective methods
		self.Bind(EVT_THREAD_TEXT_EVENT, self.ThreadTextInfo)
		self.Bind(EVT_STATUS_BAR_EVENT, self.StatusTextInfo)
		self.Bind(EVT_GAUGE_EVENT, self.StatusBar)
        

		

		
		self.SetSizerAndFit(sizer)
		
		
		
					
	def OnQuit(self, e):
		self.Close()
	
	def OnThreadText(self, evt):
		msg = evt.getText()
		self.text_info.AppendText(msg + '\n')

	def ThreadTextInfo(self, e):
		msg = e.getText()
		self.text_info.AppendText(msg + '\n')
		e.Skip()

	def StatusTextInfo(self, e):		
		e.Skip()
		
	def StatusBar(self, e):
		count = e.getValue()
				
		#send the progress value to the status bar
		self.gauge.SetValue(count)
		e.Skip()
		
        
        
	def Scanner(self, e):
		if self.scan_button.GetValue():
			#check for the type of scan
			self.scan_type = self.check.IsChecked()
		
			#pull the ip address out of text field
			ipaddress = self.text.GetValue()
		
			#pull the timeout delay
			timeout = self.timeout.GetValue()
			try:
				timeout = int(timeout)
			except ValueError:
				self.text_info.AppendText('ERROR, Timeout value must be integer'+'\n')
				return
		
			self.t = PortScan(ipaddress, timeout, self.scan_type, self.gauge, self)
			self.t.start()
			
			self.scan_button.SetLabel('Stop')
			
		else:
			self.text_info.AppendText('Stopping...')
			self.t.stop()
			self.scan_button.SetLabel('Scan')
		
		
	def OnKeyDown(self, e):        
		key = e.GetKeyCode()        
		if key == wx.WXK_ESCAPE:            
			ret  = wx.MessageBox('Are you sure to quit?', 'Question', 
			wx.YES_NO | wx.NO_DEFAULT, self)                
			if ret == wx.YES:
				self.Close()	
		            
  
