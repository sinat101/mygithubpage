#!/usr/bin/env python
import subprocess
import sys
import copy

##	By: Sina Taghizadehmoghadam


while True:

	# Clear the screen
	subprocess.call('clear', shell=True)

	# Basic list of all routers in the network
	routers = {'t':None, 'u':None, 'v':None, 'w':None, 'x':None, 'y':None, 'z':None}

	# The given network simulated in nested dictionaries in Python
	network = {
	't':{'u':2, 'v':4, 'y':7},
	'u':{'t':2, 'v':3, 'w':3},
	'v':{'t':4, 'u':3, 'w':4, 'x':3, 'y':8},
	'w':{'u':3, 'v':4, 'x':6},
	'x':{'v':3, 'w':6, 'y':6, 'z':8},
	'y':{'t':7, 'v':8, 'x':6, 'z':12},
	'z':{'x':8, 'y':12}
	}

	# The biggest possible integer value in Python, which will simulate infinity
	inf = sys.maxint

	# The outline of a cost table for each router
	table_costs = {'t':inf, 'u':inf, 'v':inf, 'w':inf, 'x':inf, 'y':inf, 'z':inf}

	# A table of the predecessor for each router in its optimal path, to be used in combination
	# with the cost table above to create the forwarding table for each router
	table_preds = {
	't':'uknown',
	'u':'uknown',
	'v':'uknown',
	'w':'uknown',
	'x':'uknown',
	'y':'uknown',
	'z':'uknown'
	}


	# Asking the user if they would like to change any of the link costs in the network
	# with error handling integrated
	while True:
			
		redo_network = raw_input("The network has been configured according to default link costs, would you like to update any of them? (yes or no)\n")

		if redo_network != 'yes' and redo_network != 'no':

			print "You must enter either 'yes' or 'no', please try again!\n"
			continue

		else:

			break

	# If the user decides to change any of the link costs, they must give two valid routers
	# that have a direct link and a new valid link cost.
	while redo_network == 'yes':

		print "**NOTE**: ONLY VALID AND DIRECT LINKS BETWEEN ROUTERS ARE ABLE TO BE CHANGED.\n"
		
		while True:
			
			# The two valid routers
			link_start = raw_input("Please enter the starting router of the link (t, u, v, w, x, y, or z):\n")
			link_end = raw_input("Please enter the end router of the link (t, u, v, w, x, y, or z):\n")
			
			if link_start not in ['t', 'u', 'v', 'w', 'x', 'y', 'z'] or link_end not in ['t', 'u', 'v', 'w', 'x', 'y', 'z']:

				print "Please enter a VALID router for the start AND end (t, u, v, w, x, y, or z).\n"
				continue

			elif link_end not in network[link_start]:

				print "You have entered an INVALID or NON-DIRECT link! Please try again!\n"
				continue

			else:

				break

		while True:

			try:
				
				# The valid new link cost
				link_cost = int(raw_input("Please enter the new cost of the link (must be positive non-zero integer):\n"))
			
			except ValueError:
		        
				print "That's not an integer, try again!\n"
				continue

			if link_cost < 1:

				print "The new link cost must be greater than or equal to 1, try again!\n"
				continue

			else:

				break

		# Updating network with the new link cost
		network[link_start][link_end] = link_cost
		network[link_end][link_start] = link_cost

		while True:
			
			# Asking if there are more link costs to update
			redo_network = raw_input("\nLink costs have been updated. Update more? (yes or no)\n")

			if redo_network != 'yes' and redo_network != 'no':

				print "You must enter either 'yes' or 'no', please try again!\n"
				continue

			else:

				break

	while True:
		
		# Asking for the source and destination to be used in calculating the optimal cost and path	
		source = raw_input("Please enter the source router (t, u, v, w, x, y, or z):\n")
		dest = raw_input("Please enter the destination router (t, u, v, w, x, y, or z):\n")
		
		if source not in ['t', 'u', 'v', 'w', 'x', 'y', 'z'] or dest not in ['t', 'u', 'v', 'w', 'x', 'y', 'z']:

			print "Please enter a VALID router for the source AND destination (t, u, v, w, x, y, or z).\n"
			continue

		elif source == dest:

			print "You have entered the same source and destination router, there is no optimal path and the cost is 0, please try again!\n"
			continue

		else:

			break

	# Iterating through all routers in the network to create their forwarding tables
	for n in routers:

		# Removing the source/initial router from its own forwarding table
		del table_costs[n]
		del table_preds[n]

		N = copy.deepcopy(table_costs)
		N_prime = {n:0}

		# Initialization step of Dijkstra's algorithm
		for init_rtr,init_cost in table_costs.iteritems():
			for network_rtr,network_cost in network[n].iteritems():
				if init_rtr == network_rtr:
					# Setting source router's forwarding table entries for its direct neighbors
					table_costs[init_rtr] = network_cost
					table_preds[init_rtr] = n

		# Looping step of Dijkstra's algorithm
		while N:
			N = copy.deepcopy(table_costs)
			for i in N_prime:
				N.pop(i, None)
			if N:
				curr_min = min(N, key=N.get)
				N_prime[curr_min]=0
				# Going through the steps of the algorithm and updating the forwarding table accordingly
				for router,cost in table_costs.iteritems():
					for curr_rtr,curr_cost in network[curr_min].iteritems():
						if router == curr_rtr and curr_rtr not in N_prime:
							temp_cost = min(cost, (table_costs[curr_min]+curr_cost))
							if temp_cost != table_costs[router]:
								table_preds[router] = curr_min
							table_costs[router] = temp_cost
		
		# Printing completed forwarding tables for the user, for each router on the network
		print "\n***FORWARDING TABLE FOR ROUTER '"+n+"'***"
		print "Router | Cost | Predecessor"
		for rtr in ['t', 'u', 'v', 'w', 'x', 'y', 'z']:
			if rtr != n:
				print '   '+rtr+'   '+'   '+str(table_costs[rtr]).zfill(3)+'   '+'     '+table_preds[rtr]
		
		# Storing the cost and predecessor tables of the user-indicated source router for later use in
		# optimal cost and path calculation
		if n == source:
			src_dest_table_costs = copy.deepcopy(table_costs)
			src_dest_table_preds = copy.deepcopy(table_preds)

		# Resetting cost table and predecessor table in preparation for next router/iteration
		table_costs = {'t':inf, 'u':inf, 'v':inf, 'w':inf, 'x':inf, 'y':inf, 'z':inf}

		table_preds = {
		't':'uknown',
		'u':'uknown',
		'v':'uknown',
		'w':'uknown',
		'x':'uknown',
		'y':'uknown',
		'z':'uknown'
		}

	# Calculating optimal cost based on saved cost table from before
	optimal_cost = src_dest_table_costs[dest]
	optimal_path = ''
	destination = dest
	# Calculating optimal path based on saved predecessor table from before
	while src_dest_table_preds[destination] != source:
		optimal_path = src_dest_table_preds[destination]+'-'+optimal_path
		destination = src_dest_table_preds[destination]

	print '\nThe optimal cost from '+source+' to '+dest+' is: '+str(optimal_cost)
	print 'The optimal path from '+source+' to '+dest+' is: '+source+'-'+optimal_path+dest+'\n'

	# Asking user if they would like to run the program again, script restarts if so
	while True:

		restart = raw_input("Would you like to run the simulation again? (yes or no)\n")

		if restart != 'yes' and restart != 'no':

			print "You must enter either 'yes' or 'no', please try again!\n"
			continue

		else:

			break

	if restart == 'yes':

		continue

	else:

		print "\nThank You and Goodbye :-)\n"
		break
