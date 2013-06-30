#!/usr/bin/env python
import Queue
import threading
import urllib2
import time
import subprocess
import socket
          

f = open('./iplist.txt', 'a')         
queue = Queue.Queue()
ip_list = []
def ping(address):
	ping = subprocess.Popen(['/bin/ping',address, '-c 1'], stderr=subprocess.STDOUT,stdout = subprocess.PIPE )
	out, err = ping.communicate()
	#print out
	if '1 received' in out:
		return True
	else:
		return False 
		
def scan(address, port): 
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
		  
class ThreadUrl(threading.Thread):
	
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
		
	def run(self):
		while True:
                #grabs host from queue
            
			host = self.queue.get()
			openport = False	
			if host == 'kill':
				break		
			response = ping(host)
			ports = ''
			if response == True:
				port_open = False
				
				ip_list.append(host)
				for port in [20, 21, 22, 23, 79, 80, 110, 113, 119, 143, 443, 1002, 1720, 5000, 8080]:
					if scan(host, port) == True:
						openport = True
						print 'open port: ', port
						ports = ports+',' + str(port)
				if openport == True:
					f.write(host+','+ports+'\n')
					print host, '<>-<>-<>-<>-<>-<>-<>-<>-OPEN--PORT-<>-<>-<>-<>-<>-<>-<>-<>'
				else:
					print host, '******************responded******************'
			else:
				print host, ' did not respond'
			self.queue.task_done()
		print 'thread closing'
			
          
start = time.time()
count = 0
def block(count):
          
            #spawn a pool of threads, and pass them queue instance 
	for i in range(300):
		
		t = ThreadUrl(queue)
		t.setDaemon(True)
		t.start()
              
           #populate queue with data
	for a in range(10,150):
		for b in range(250, 300):
			for c in range(1, 10):
				for i in range(1, 10):
					address = str(a) + '.' +str(b) + '.' + str(c) + '.' + str(i)
					queue.put(address)
					count = count + 1  
		
           
           #wait on the queue until everything has been processed     
	queue.join()
	#for i in range(300):
	#	queue.put('kill')
	return count


count = block(count)
f.close()
	          


print count, " ips scanned"
print "Elapsed Time: %s" % (time.time() - start)
print count / (time.time() - start), ' ips/sec'
