import threading
import socket
import os
import subprocess
import wx

from NewTextEvent import NewTextEvent
from NewIntEvent import NewIntEvent

from Status import gaugeEventType
from Status import EVT_GAUGE_EVENT

from PanelMessage import PanelMessage

	  
class IPScanThread(threading.Thread):
	
	def __init__(self, queue, status, output_window, log_level):
		threading.Thread.__init__(self)
		
		#Queue instance from parent
		self.queue = queue
		
		#object instance of statuse class from parent
		self.status = status
		
		#reference to panel 
		self.output_window = output_window
		
		#Start an instance of the function to send messages to panel
		self.message = PanelMessage(output_window)
		
		#self.message.send('thread started')
		
		self.running = True
		
		#verbose level
		self.log_level = log_level
		
	def ping(self, address):
		ping = subprocess.Popen(['/bin/ping',address, '-c 1'], stderr=subprocess.STDOUT,stdout = subprocess.PIPE )
		out, err = ping.communicate()
		if '1 received' in out:
			return True
		else:
			return False 
		
	def scan(self, address, port): 
		s = socket.socket()
		s.settimeout(2) 
		try: 
			s.connect((address, port)) 				
			return True 
		except socket.error, e: 
			return False
		s.close()  
		
	def stop(self):
		self.running = False      
		
	def run(self):
		while self.running:
               
                #grabs host from queue            
			host = self.queue.get()
			openport = False	
			if host == 'kill':
				break		
			response = self.ping(host)
			ports = ''
			if response == True:				
				for port in [20, 21, 22, 23, 79, 80, 110, 113, 119, 143, 443, 1002, 1720, 5000, 8080]:
					if self.scan(host, port) == True:
						openport = True						
						ports = ports+',' + str(port)
				if openport == True:
					self.message.send(host+' <>-<>-OPEN PORT-<>-<>')					
				else:
					if self.log_level >= 1:
						self.message.send(host+' ******RESPONDED******')					
			else:
				if self.log_level >= 2:
					self.message.send(host+' did not respond')				
			self.status.add()	
			self.queue.task_done()		
