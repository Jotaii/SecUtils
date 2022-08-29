#!/bin/python3

import sys
import socket
import threading
from datetime import datetime as dt


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def scanner(IP, PORT, args = []):
	if '-v' in args:
		print("Checking port {} from {}".format(PORT, IP))
	target = socket.gethostbyname(IP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(1)
	result = s.connect_ex((target, PORT))
	if result == 0:
		print("Port {} is open".format(PORT))
	s.close()
	

if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #IPv4
	num_threads = 1

elif len(sys.argv) == 4 and "-t" in sys.argv:
	try:
		target = socket.gethostbyname(sys.argv[1]) #IPv4
		num_threads = int(sys.argv[sys.argv.index('-t')+1])
		
	except ValueError:
		print("Invalid value for -t parameter, only integers admited")
		sys.exit()

else:
	print("Invalid amount of arguments")
	print("Syntax: python3 portScanner.py <ip> ")
	sys.exit()
	
#banner
print("-" * 50)
print("Scanning target " + target)
print("\tthreads: ", num_threads)
print("\tverbose: ", ('-v' in sys.argv))
time_started = dt.now()
print("Time started " + str(time_started))
print("-" * 50)

try:
	threads = []
	counter = 0
	for port in range(1,65536, num_threads):
		sup_limit = port+200
		if sup_limit > 65536:
			sup_limit = 6536
			
		for pid in range(port,sup_limit):
		#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#socket.setdefaulttimeout(1)
		#result = s.connect_ex((target, port))
		#if result == 0:
		#	print("Port {} is open".format(port))
		#s.close()
			t = threading.Thread(target=scanner, args=[target, pid, sys.argv])
			t.start()
			threads.append(t)
			
		for thread in threads:
			thread.join()
		
		threads = []
		counter += 1
		printProgressBar(counter, 65536//num_threads)
		
except KeyboardInterrupt:
	print ("\nExiting program.")
	sys.exit()
	
except socket.gaierror:
	print("Hostname could not be resolved.")
	sys.exit()

except socket.error:
	print("Couldn't connect to server.")
	sys.exit()
	
#banner
print("\n\n\n")
print("-" * 50)
print("Ports Scanned")
time_end = dt.now()
print("Time end " + str(time_end))
print("Time elapsed ", str(time_end - time_started)) 
print("-" * 50)

