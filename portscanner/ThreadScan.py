import socket
import subprocess
import sys
import Queue
import threading


class ThreadScan(threading.Thread):
	
	def __init__(self, queue, host, port_list, timeout, status):
		threading.Thread.__init__(self)
		self.queue = queue
		self.host = host
		self.timeout = timeout
		self.port_list = port_list
		self.status = status
		
	def scan_server(self, address, port): 
		s = socket.socket()
		s.settimeout(self.timeout) 		
		try: 
			s.connect((address, port)) 			
			self.port_list.append(port)
			return True 
		except socket.error, e: 			
			return False
		s.close() 
		
		
	def run(self):
		while True:
			
                #grabs host from queue
			port= self.queue.get()
			if port == 123456789:
				break
			self.scan_server(self.host, port)
			self.status.add()
			self.queue.task_done()
		
