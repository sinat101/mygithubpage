#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

##############################################################################################
##	This script is built upon the original script located here:

##	http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python

##	It adds the ability to specify what range of ports to scan and does error handling for it,
##	along with error handling for the hostname/IP input at the beggining, instead of the end.

##	With the error handling, it does not simply exit if something is entered wrong, but lets
##	the user try again.

##	It also specifies if a port is closed, not just if it is open.
##############################################################################################

##	By: Sina Taghizadehmoghadam


# Clear the screen
subprocess.call('clear', shell=True)

# Asking for hostname or IP to scan
while True:

	try:

		remoteServer    = raw_input("Enter a valid hostname or IPv4 address to scan: ")
		remoteServerIP  = socket.gethostbyname(remoteServer)

	except socket.gaierror:

		print "Invalid hostname or IP, try again!"
		continue

	else:

		break

#Getting the start value for the port range to scan
while True:

	try:
		
		portRangeStart = int(raw_input("Enter valid port for start of range: "))

	except ValueError:

		print "That's not an integer, try again!"
		continue

	if portRangeStart > 65535 or portRangeStart < 1:

		print "Sorry, that's not a valid port number, try again!"
		continue

	else:

		break

#Getting the end value for the port range to scan
while True:

	try:
		
		portRangeEnd = int(raw_input("Enter valid port for end of range: "))
	
	except ValueError:
        
		print "That's not an integer, try again!"
		continue

	if portRangeEnd > 65535 or portRangeEnd < 1:
    	
		print "Sorry, that's not a valid port number, try again!"
		continue

	elif portRangeEnd < portRangeStart:

		print "The end of your port range cannot be less than the start, try again!"
		continue

	else:

		break


# Print a nice banner with information on which host we are about to scan
print "-" * 85
print "Please wait, scanning remote host", remoteServerIP, "on ports", portRangeStart, "through", portRangeEnd
print "-" * 85

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (from user input above)

# We also put in some error handling for catching errors

try:
	for port in range(portRangeStart,portRangeEnd+1):  
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((remoteServerIP, port))
		if result == 0:
			print "Port {}: \t Open".format(port)
		else:
			print "Port {}: \t Closed".format(port)
		sock.close()

except KeyboardInterrupt:
	print "\nYou pressed Ctrl+C"
	sys.exit()

except socket.error:
	print "Couldn't connect to server"
	sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total = t2 - t1

# Printing the information to screen
print 'Scanning Completed in: ', total

