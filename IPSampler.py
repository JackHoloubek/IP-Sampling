#!/usr/bin/env python

import re
import sys
import csv
import argparse


"""
This script takes aqcout file with job 1 being an SP calculation at ground state followed by job 2 as an SP in the oxidized state.
The script also reads the $comment section to read the atom info as output by the bgf to qcin scipt.
"""

prefix = sys.argv[1]
if '.qcin' in prefix:
	prefix = prefix.replace('.qcin','')
infile = prefix + '.qcout'
#print(prefix,infile)
###################################### READ QCOUT FILE #############################################################################################################################################################################

with open(infile) as f:
	chelplines = f.readlines()
	
	job1lines = [] #Atom ChelpG charges from parsing job 1
	job2lines = [] #Atom ChelpG charges from parsing job 1
	reslines = []  #Atom resnames from comment section
	Energy = []
	Charge = []
	job1 = 0 #Status modifier to divide jobs
	job2 = 0 #Status modifier to divide jobs
	recordatom = 0 #Status modifier to record atoms
	comment = 0 #Status modifier to record resnames

#Record each line of chelpg lines and save it as list chelplines[]

	for i, line in enumerate(chelplines):

####################################### LOOK FOR RELEVANT INFO ###################################################################################################################################################################
		if line.startswith('$comment'):
			comment = 1
		if comment == 1 and line.startswith('$end'):
			comment = 0
		elif comment == 1:
			reslines.append(chelplines[i])

		if line.startswith('Running Job 1'):
			job1 = 1
			
		if line.startswith('Running Job 2'):
			job2 = 1
			job1 = 0


		if line.startswith('         Ground-State ChElPG Net Atomic Charges'):
			recordatom = 1
			

		elif recordatom==1 and (line.startswith('  Sum of atomic charges =    ')):
			Charge += re.findall(r"([\d\.\-]+)", line)
			recordatom = 0

		elif recordatom==1:
			if job1 == 1:
				job1lines.append(chelplines[i])
			elif job2 == 1:
				job2lines.append(chelplines[i])

	 #Save the energy of the molecule
		elif (line.startswith(' Total energy in the final basis set =')):
			Energy += re.findall(r"([\d\.\-]+)", line)			

########################################### SPLIT EACH LINE INTO ELEMENTS AND SAVE THE RELEVANT ONES IN LISTS ######################################################################################################################
	
		
	resnames = []
	j1atomtype = []
	j2atomtype = []
	j1atomq = [] 
	j2atomq = []
	del job1lines[0:3]; del job1lines[-1] 
	del job2lines[0:3]; del job2lines[-1] 
	del reslines[0]
	

	a=0
	while a < len(job1lines):
		#print(a,job1lines[a])
		reselement = re.findall(r'\S+',reslines[a])
		
		j1elements = re.findall(r'\S+',job1lines[a])
		j2elements = re.findall(r'\S+',job2lines[a])

		resnames.append(reselement[1])		

		
		j1atomtype.append(j1elements[1])
		j1atomq.append(j1elements[2])
		
		j2atomtype.append(j2elements[1]) 
		j2atomq.append(j2elements[2])
		a+=1

		
	#print(j1atomtype,j1atomq,j2atomtype,j2atomq)

################################################ CALCULATE CHARGE OF EACH RESNAME ######################################################################################################################################################
# First find unique resnames

	unique_resname = []
	job1q = [] # a list equal to length of unique resname with the sum of all atoms matching said resname from job 1
	job2q = [] # a list equal to length of unique resname with the sum of all atoms matching said resname from job 2
	deltaq =[] # a list equal to length of unique resname for the change in charge between each residue


     
    # traverse for all elements
	for x in resnames:
		if x not in unique_resname:
			unique_resname.append(x)

	#print(unique_resname)
	a=0
	while a < len(unique_resname):
		b=0
		j1resq = 0 # value to add up all atom charges of equal resname
		j2resq = 0 # value to add up all atom charges of equal resname
		while b < len(j1atomtype):
			if resnames[b] == unique_resname[a]:
				
				j1resq += float(j1atomq[b])
				j2resq += float(j2atomq[b])
			b+=1

		job1q.append(j1resq)
		job2q.append(j2resq)
		deltaq.append(round(j2resq-j1resq,3))
		a+=1

	#print(job1q, job2q, deltaq)
#Calculate the IP in eV from the values

E1 = float(Energy[1])
E0 = float(Energy[0])
#Calculate IP in eV
IP = round((E1 - E0)*27.2114,3)

with open('IPData.dat', "a") as f2:
	f2.write(infile + ", " + str(IP))
	a=0
	while a < len(deltaq):
		
		f2.write(", " + unique_resname[a] + ", " + str(deltaq[a]))
		a+=1
	f2.write('\n')
	f2.close()
print ("Done with "+infile)

