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

#from IPScanner import TextEventType
#from IPScanner import EVT_THREAD_TEXT_EVENT

#from IPScanner import StatusEventType
#from IPScanner import EVT_STATUS_BAR_EVENT



	  
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
		
		#verbose
		self.log_level = log_level
		
	def ping(self, address):
		ping = subprocess.Popen(['/bin/ping',address, '-c 1'], stderr=subprocess.STDOUT,stdout = subprocess.PIPE )
		out, err = ping.communicate()
		#print out
		if '1 received' in out:
			return True
		else:
			return False 
		
	def scan(self, address, port): 
		s = socket.socket()
		s.settimeout(2) 
	#print 'Scanning\t', port 
		try: 
			s.connect((address, port)) 
		#print port, '\t Open' 
		
			return True 
		except socket.error, e: 
			#print port, '\t Closed' 
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
				#ip_list.append(host)
				for port in [20, 21, 22, 23, 79, 80, 110, 113, 119, 143, 443, 1002, 1720, 5000, 8080]:
					if self.scan(host, port) == True:
						openport = True
						print 'open port: ', port
						ports = ports+',' + str(port)
				if openport == True:
					self.message.send(host+' <>-<>-OPEN PORT-<>-<>')
					#f.write(host+','+ports+'\n')
					print host, '<>-<>-<>-<>-<>-<>-<>-<>-OPEN--PORT-<>-<>-<>-<>-<>-<>-<>-<>'
				else:
					if self.log_level >= 1:
						self.message.send(host+' ******RESPONDED******')
					print host, '******************responded******************'
			else:
				if self.log_level >= 2:
					self.message.send(host+' did not respond')
				print host, ' did not respond'
			self.status.add()	
			self.queue.task_done()
		print 'thread closing'
