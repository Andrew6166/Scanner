#!/usr/bin/env python
import wx
from portscanner.PortScannerPanel import PortScannerPanel
from ipscanner.IPScannerPanel import IPScannerPanel

from portscanner.PortScanner import StatusEventType
from portscanner.PortScanner import EVT_STATUS_BAR_EVENT

class MainFrame(wx.Frame):
	def __init__(self, parent, *args, **kwargs):
		wx.Frame.__init__(self, parent, title="Port Scanner", size=(600,500), *args, **kwargs)
		framesizer = wx.BoxSizer(wx.VERTICAL)
        
        #Set the desired window size
		framesizer.SetMinSize((600,500))
        
        #create the portscanner panel
		self.panel = PortScannerPanel(self)
        
		#ip scanner panel
		self.IPpanel = IPScannerPanel(self)
		self.IPpanel.Hide()
        
        #add the panel to the window
		framesizer.Add(self.panel, 1, wx.EXPAND )		
		framesizer.Add(self.IPpanel, 1, wx.EXPAND )
		
		
        
        #set up the menu bar
		menubar = wx.MenuBar()
        
        #add the file menu 
		fileMenu = wx.Menu()
		fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
		menubar.Append(fileMenu, '&File')
        
        #add the view menu
		viewMenu = wx.Menu()
		switch_panels = viewMenu.Append(wx.ID_ANY, 'Switch Panels', 'switch between port/ip scanner')
		menubar.Append(viewMenu, '&View')
        
        
		self.SetMenuBar(menubar)		
        
        #bind the panel switcher tio its method
		self.Bind(wx.EVT_MENU, self.onSwitchPanels, switch_panels)
        
        #bind the status bar update to the method
		self.Bind(EVT_STATUS_BAR_EVENT, self.StatusTextInfo)
        
        #bind the quit button on the menu
		self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        
        #creat the status bar
		self.sb = self.CreateStatusBar()
        
        #self.SetSize((600,500))
        
		self.SetSizerAndFit(framesizer)
        
		self.Centre()
		self.Show(True)
        
	def OnQuit(self, evt):
		self.Close()
		
	def StatusTextInfo(self, e):
		msg = e.getText()
		self.sb.SetStatusText(msg)
		e.Skip()
		
	def onSwitchPanels(self, e):
		if self.panel.IsShown():
			self.SetTitle("IP Scanner")
			self.panel.Hide()
			self.IPpanel.Show()
		else:
			self.SetTitle("Port Scanner")
			self.panel.Show()
			self.IPpanel.Hide()
		self.Layout()

    



if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None)
    frame.Show(True)

    app.MainLoop()
