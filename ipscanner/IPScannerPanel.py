
import socket
import subprocess
import sys
import Queue
import threading
import time
import wx
from IPScanner import IPScan
from IPScanThread import IPScanThread

from Status import gaugeEventType
from Status import EVT_GAUGE_EVENT

from PanelMessage import TextEventType
from PanelMessage import EVT_THREAD_TEXT_EVENT

from IPScanner import StatusEventType
from IPScanner import EVT_STATUS_BAR_EVENT

import wx


TASK_RANGE = 100




class IPScannerPanel(wx.Panel):
           
	def __init__(self, parent, *args, **kw):
		wx.Panel.__init__(self, parent, size=(600,500),*args, **kw)
                
		self.InitUI()
		
		self.loglevel = 1
        
	def InitUI(self):   

		
		
		#sizer
		sizer = wx.GridBagSizer(4, 4)
		
	
		#title text
		font1 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		name = wx.StaticText(self, label="IP Scanner")
		name.SetFont(font1)
		sizer.Add(name, pos=(0,2), flag=wx.TOP|wx.BOTTOM, border = 5)
		
				
		#button to start scan
		self.scan_button = wx.ToggleButton(self, label='Scan')
		sizer.Add(self.scan_button, pos=(1,0), flag=wx.LEFT, border=5) 
        
        #label for the host field		
		label = wx.StaticText(self, label='From')
		sizer.Add(label, pos=(1,1), flag=wx.LEFT, border=10)
		
		
		
		#IP address range ip1 a.b.c.d ip1a, ip1b, ip1c, ip1d
		
		#IP address 1 a to d
		self.ip1a = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip1a, pos=(1,2))
		
		
		self.ip1b = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip1b, pos=(1,3))

		
		self.ip1c = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip1c, pos=(1,4))

		
		self.ip1d = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip1d, pos=(1,5))
		
		
		#to label		
		label2 = wx.StaticText(self, label='To')		
		sizer.Add(label2, pos=(2,1), flag=wx.LEFT, border=10)
		
		#IP address 2 from a to d
		self.ip2a = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip2a, pos=(2,2))
		
		
		self.ip2b = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip2b, pos=(2,3))
		
		
		self.ip2c = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip2c, pos=(2,4))
		
		
		self.ip2d = wx.TextCtrl(self,  style=wx.TE_PROCESS_ENTER)
		sizer.Add(self.ip2d, pos=(2,5))
		
		#combo box for how verbose
		self.options = ['Open Ports', 'Responses', 'All']
		self.combo = wx.ComboBox(self, size=(90, 30 ), choices=self.options, style=wx.CB_READONLY)
		sizer.Add(self.combo, pos=(3,3))
		
				
		
        		
		#Label for timeout box
		timeout = wx.StaticText(self, label='Timeout', )
		sizer.Add(timeout, pos=(3,1), flag=wx.LEFT, border = 20)
		
		#Field for timeout
		self.timeout = wx.TextCtrl(self, size=(90,30))
		sizer.Add(self.timeout, pos=(3,2), flag=wx.RIGHT|wx.LEFT, border=5)
		
		#initialize with a default value of 2
		self.timeout.SetValue('2')
        
        
        #Field for displaying the output from the scanner, readonly
		self.text_info = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY|wx.TE_AUTO_URL)
		sizer.Add(self.text_info, pos=(4,0), span=(3,10), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)      
        
        #status bar 
		self.gauge = wx.Gauge(self, range=TASK_RANGE)
		sizer.Add(self.gauge, pos=(7,0), span=(1,10), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)       
		
		#set expandable rows and columns
			
		sizer.AddGrowableRow(4)
		sizer.AddGrowableCol(9)		
		
		#Exit key bindings
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		
		#combo box bindings
		self.combo.Bind(wx.EVT_COMBOBOX, self.onSelect)
		
		#bind button to method to call port scanner
		self.scan_button.Bind(wx.EVT_TOGGLEBUTTON, self.Scanner)
		
				
        
        #bind the custom events for updating status bar, text window, gauge to respective methods
		self.Bind(EVT_THREAD_TEXT_EVENT, self.ThreadTextInfo)
		self.Bind(EVT_STATUS_BAR_EVENT, self.StatusTextInfo)
		self.Bind(EVT_GAUGE_EVENT, self.StatusBar)        
	
		self.SetSizerAndFit(sizer)
		
		
	def onSelect(self, e):
		i = e.GetString()
		self.loglevel = self.options.index(i) 
					 
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
			iprange = {'ip1a':int(self.ip1a.GetValue()), 'ip1b':int(self.ip1b.GetValue()),
						'ip1c':int(self.ip1c.GetValue()), 'ip1d':int(self.ip1d.GetValue()),
						'ip2a':int(self.ip2a.GetValue()), 'ip2b':int(self.ip2b.GetValue()),
						'ip2c':int(self.ip2c.GetValue()), 'ip2d':int(self.ip2d.GetValue())}
						
			self.t = IPScan(self, iprange, self.loglevel)
			self.t.start()
			
			self.scan_button.SetLabel('Stop')
			
		else:
			self.t.stop()
			self.scan_button.SetLabel('Scan')
		
		
		
	def OnKeyDown(self, e):        
		key = e.GetKeyCode()        
		if key == wx.WXK_ESCAPE:            
			ret  = wx.MessageBox('Are you sure to quit?', 'Question', 
			wx.YES_NO | wx.NO_DEFAULT, self)                
			if ret == wx.YES:
				self.Close()
					 
		
	
