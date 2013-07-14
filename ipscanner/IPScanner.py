
import Queue
import threading
import time
import subprocess
import socket
import wx
from Status import Status
from IPScanThread import IPScanThread
from NewTextEvent import NewTextEvent
from NewIntEvent import NewIntEvent
from PanelMessage import PanelMessage
from Status import gaugeEventType
from Status import EVT_GAUGE_EVENT
          
TextEventType = wx.NewEventType()
EVT_THREAD_TEXT_EVENT = wx.PyEventBinder(TextEventType, 1)

StatusEventType = wx.NewEventType()
EVT_STATUS_BAR_EVENT =wx.PyEventBinder(StatusEventType, 1)


class IPScan(threading.Thread):
	def __init__(self,  output_window, iprange, loglevel):
		threading.Thread.__init__(self)	
		#set up the message write to the panel
		self.message = PanelMessage(output_window)
		
		#iprange
		self.iprange = iprange
		
				
		#creat queue for consumer threads
		self.queue = Queue.Queue()		
		
		#initialize empty array for sortage of ip list
		self.ip_list = []
		
		#parent window
		self.output_window = output_window
		
		#creat empty array for all the ip addresses we will scan
		self.ips_to_scan = []
		
		#list to contain all the threeads generated
		self.threads = []
		
		#verbose
		self.log_level = loglevel
		
		#flag to see if stop scan was called
		self.stopped = False
		
				
	def run(self):
		self.Scan()
		
	def stop(self):
		self.stopped = True
		self.message.send('stopping')
								
		for thread in self.threads:
			thread.stop()		
			
		for thread in self.threads:
			thread.join()	
						
		self.message.send('all threads closed')
			
		self.status.reset()
		
		
	def makeIPlist(self):
		for a in range(self.iprange['ip1a'],self.iprange['ip2a']):
			for b in range(self.iprange['ip1b'], self.iprange['ip2b']):
				for c in range(self.iprange['ip1c'], self.iprange['ip2c']):
					for i in range(self.iprange['ip1d'], self.iprange['ip2d']):
						address = str(a) + '.' +str(b) + '.' + str(c) + '.' + str(i)
						self.ips_to_scan.append(address)
						
						#count = count + 1  
		
			
	def Scan(self):
		#starting time
		self.start = time.time()
				
		self.message.send('scanning')
		
		print 'starting'
		count = 0
		self.makeIPlist()
		list_length = len(self.ips_to_scan)
		self.message.send(str(list_length)+' ips on scan list')
		
		self.status = Status(list_length, self.output_window)
			
			#spawn a pool of threads, and pass them queue instance 
		for i in range(200):
			t = IPScanThread(self.queue, self.status, self.output_window, self.log_level)
			t.setDaemon(True)
			t.start()
			self.threads.append(t)
				
				#populate queue with data
		for thread in self.threads:
			print thread
		
		for address in self.ips_to_scan:
			self.queue.put(address)
			
								
								
				#wait on the queue until everything has been processed     
		self.queue.join()
		
		if self.stopped == False:		
				#poison pills
			for i in range(300):
				queue.put('kill')
			
		self.message.send("threads killed")
				
				#calculate total time on process
		self.totaltime = time.time() - self.start				
			

