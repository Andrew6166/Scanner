#!/usr/bin/env python
import wx
from portscanner.PortScannerPanel import PortScannerPanel

from portscanner.PortScanner import StatusEventType
from portscanner.PortScanner import EVT_STATUS_BAR_EVENT

class MainFrame(wx.Frame):
	def __init__(self, parent, *args, **kwargs):
		wx.Frame.__init__(self, parent, size=(600,500), *args, **kwargs)
		framesizer = wx.BoxSizer(wx.VERTICAL)
        
        #Set the desired window size
		framesizer.SetMinSize((600,500))
        
        #create the portscanner panel
		self.panel = PortScannerPanel(self)
        
        #add the panel to the window
		framesizer.Add(self.panel, 1, wx.EXPAND )
        
        #set up the menu bar
		menubar = wx.MenuBar()
        
        #add the file menu 
		fileMenu = wx.Menu()
		fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
		menubar.Append(fileMenu, '&File')
        
        #add the view menu
		viewMenu = wx.Menu()
		menubar.Append(viewMenu, '&View')
        
        
		self.SetMenuBar(menubar)		
        
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

    



if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="Change Panel Color Custom Event")
    frame.Show(True)

    app.MainLoop()
