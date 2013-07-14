########################################################################
#	Creator: Russell Loewe
#	Contact: russloewe@gmail.com
#	Purpose: Multi-Threaded port scanner
#	Depends on : ThreadScan.py
#	Use-age: Example at bottom of script 
#	Notes  : This class is set up to for use with python wx
#	To-Do  : Change class name to Scanner, method to Scan()
#
########################################################################
import socket
import subprocess
import sys
import Queue
import threading
import time
from PanelMessage import PanelMessage
from ThreadScan import ThreadScan
from Status import Status
from NewTextEvent import NewTextEvent
from NewIntEvent import NewIntEvent
import wx

from Status import gaugeEventType
from Status import EVT_GAUGE_EVENT

TextEventType = wx.NewEventType()
EVT_THREAD_TEXT_EVENT = wx.PyEventBinder(TextEventType, 1)

StatusEventType = wx.NewEventType()
EVT_STATUS_BAR_EVENT =wx.PyEventBinder(StatusEventType, 1)





		
class PortScan(threading.Thread):
	def __init__(self, host, timeout, full_scan, gauge, output_window):
		threading.Thread.__init__(self)		
		
		#pull the wx frame for the info box event		
		self.output_window = output_window
		
		#creat messanger object for sending text to panel
		self.message = PanelMessage(output_window)
		
		#get gauge instance from gui
		self.gauge = gauge
				
		#get host
		self.host = host
		
		#boolean to indicate if the scan will do all ports or the smaller set
		self.full_scan = full_scan
		
		#queue to pass ports to threads
		self.queue = Queue.Queue()
		
		#empty array that will hold the list of open ports
		self.port_list = []
		
		#counter to caluclate ports scasnned per second
		self.count = 0
		
		#passed to threads, how long to wait on port response
		self.timeout = timeout
		
		#how many threads to run concurently
		self.threadcount = 200
		
		#list to contain all the threeads generated
		self.threads = []
		
		#range of ports to scan, set 9999 as default, but changed later if needed
		self.portrange = 9999
		
		#list of common ports for the shart scan
		self.common_ports = [20, 21, 22, 23, 79, 80, 110, 113, 119, 143, 443, 1002, 1720, 5000, 8080]
		
		#start Status object, pass actule number of ports to be scanned
		#change some variables depending on the type of scan chosen
		if self.full_scan == True:
			self.status = Status(self.portrange-1, self.output_window)			
		else:
			self.portrange = len(self.common_ports)	
			self.status = Status(self.portrange, self.output_window)
			self.threadcount = self.portrange
			
	def run(self):
		self.Scan()
		
	def stop(self):
		self.message.send('stopping')		
				
		for thread in self.threads:
			thread.stop()		
			
		for thread in self.threads:
			thread.join()	
						
		self.message.send('all threads closed')
			
		#self.status.reset()
	
	def Scan(self):
		self.start = time.time()
		
		#Send info to text window via our text event
		evt = NewTextEvent(TextEventType, -1)
		evt.setText('Scanning host: ' + self.host + ' over '+ str(self.portrange) + ' ports, with a timeout of ' + str(self.timeout))
		wx.PostEvent(self.output_window, evt)
		
		#send message to status bar
		evt2 = NewTextEvent(StatusEventType, -1)
		evt2.setText('Scanning...')
		wx.PostEvent(self.output_window, evt2)
		
		#output for terminal				
		print 'Scanning host: ', self.host, ' over ',self.portrange, ' ports, with a timeout of ',self.timeout 
		
		#Generate all the consumer threads, pass the queue object,
		#the host, reference to port_list array, timeout criteria, and 
		#status object instance 			
		for i in range(self.threadcount):			
			t = ThreadScan(self.queue, self.host, self.port_list, self.timeout, self.status)
			t.setDaemon(True)
			t.start()
			self.threads.append(t)
		
		
		#fill queue with ports needing to be scanned depending on type
		#long scan
		if self.full_scan == True:
			for a in range(1,self.portrange):
				self.queue.put(a)
				self.count = self.count + 1
				
		#short scan
		elif self.full_scan == False:
			for a in self.common_ports:
				self.queue.put(a)
				self.count = self.count + 1 
           
        #wait on the queue until everything has been processed     
		self.queue.join()
		
		#send poison pills to kill threads. If the threads aren't killed
		#then if this class is run multiple times, the threads will exceed
		#limit		
		for a in range(self.threadcount):
			self.queue.put(123456789)
		
		#wait for threads to die, not working right now	, not sure if need
		#self.queue.join()
		
		#recored ending time
		self.end = time.time()
		
		#send message to status bar
		evt2 = NewTextEvent(StatusEventType, -1)
		evt2.setText('Scan done')
		wx.PostEvent(self.output_window, evt2)
		
		#reset progress bar 
		evt3 = NewIntEvent(gaugeEventType, -1)
		evt3.setValue(0)
		wx.PostEvent(self.output_window, evt3)
		
		#build a string with the host name and open ports for writing to disk
		self.Data()
		
		#call the method for handling gui elements
		self.GUIReport()
		
	
	def GUIReport(self):
		#format data for the text box and update gui fields		
		ports = ''
		
		#order the ports in the list
		self.port_list.sort()	
		
		#read threw though the list	
		for i in self.port_list:
			self.data = self.data + ';' + str(i)
			ports = ports + str(i) + '   '
			
		#stuff for stats
		totaltime = self.end - self.start
		
		#get all the info into strings
		gui_ports = 'Open Ports: ' + ports					
		ports_scanned = '\n'+str(self.count)+' ports scanned'
		elapsed_time = '\n'+'Elapsed Time: '+ str(round(totaltime, 1))+' secs'
		ports_per_sec = '\n'+str(round(self.count/totaltime,1)) +' ips/sec'
		
		#put it all together, put new line on end so next scan is seperated
		msg = gui_ports + ports_scanned + elapsed_time + ports_per_sec + '\n'
		
		#send to text window with event handler
		evt = NewTextEvent(TextEventType, -1)
		evt.setText(msg)
		wx.PostEvent(self.output_window, evt)	
	
	def Data(self):
		#process the data into easy to save format
		self.data = self.host 
		for i in self.port_list:
			self.data = self.data + ';' + str(i)
	

		 
	

#Usage example
if __name__ == "__main__":
	host = raw_input('Host:')
	scan_type = raw_input('Full scan?(y/n): ')
	
	while True:
		if scan_type == 'y':
			scanner = Scan(host, True)
			break
		elif scan_type == 'n':
			scanner = Scan(host, False)
			break
		else:
			scan_type = raw_input('please type y or n: ')
	
	scanner.scan()
	print scanner.port_list
	print scanner.data	
	scanner.results()
