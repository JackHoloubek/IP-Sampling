#!/usr/bin/env python

import re
import sys
import csv
import argparse


"""
This script takes a bgf and copies the relevant info to a qchem input file. The script then displays the atom's resname in the 
"""

prefix = sys.argv[1]
exch = sys.argv[2]
basis = sys.argv[3]
dielec = sys.argv[4]

#Define charge and multiplicity
q = 0
mult = 1



infile=prefix
outfile=prefix+'.'+basis+'.qcin'
outfile=outfile.replace('.bgf','')


###################################### READ BGF FILE #############################################################################################################################################################################

with open(infile) as f, open('Templates/InTemplate.qcin') as f1:
	bgflines = f.readlines()
	template = f1.read()
	atomlines = []
	recordatom = 0 #Status modifier to record atoms

#Record each line and save it as list atomlines[]

	for i, line in enumerate(bgflines):
		if line.startswith('FORMAT ATOM'):
			recordatom = 1
		elif line.startswith('FORMAT CONECT'):
			recordatom = 0
		elif recordatom==1:
			atomlines.append(bgflines[i])


	a=0
	atomnum = []
	atomtype = []
	type = []
	resname = []
	atomx = []
	atomy = []
	atomz = []
	atomq = []
	
	while a < len(atomlines):
		#print(atomlines[a])
		elements = re.findall(r'\S+',atomlines[a])			

######################## Define each field of interest and record it in a list with same index as atomline ################
	
		atomnum.append(elements[1])
	
		#save atomtypes without numbers
		type.append(elements[2])
		atomtype.append(''.join([i for i in type[a] if not i.isdigit()]))
		
		resname.append(elements[3])
		atomx.append(float(elements[6]))
		atomy.append(float(elements[7]))
		atomz.append(float(elements[8]))
		atomq.append(float(elements[12]))
		
		a+=1
	#total charge is sum of atom charges rounded to 1 digit
	
	q=round(sum(atomq))


######################## Find number of unique resnames and abort if = 1 ####################################################
	unique_resname = []
     
    # traverse for all elements
	for x in resname:
		if x not in unique_resname:
			unique_resname.append(x)

	#if len(unique_resname) == 1:
		#print(infile + " doesn't have enough fragments! ABORTING")
		#exit()
    # print list
	print('Fragments will be divided by:', end = " ")
	for x in unique_resname:
		print(x, end = " ")


###################################### WRITE FILE ################################################################################################################################################################################

s=template.format(charge=q, mult=mult, exch=exch, basis=basis, dielec=dielec)

############ Write the qchem settings ##########################################################

with open(outfile, "w") as f2:
	f2.write(s)
	f2.close()

############ Write the molecule, divided in separate fragments by resname ######################

with open(outfile, "a") as f2, open('Templates/AppendTemplate.qcin') as f3:
	
	for x in range (0,len(resname)):
		f2.write(atomtype[x]+"   "+str(atomx[x])+"   "+str(atomy[x])+"   "+str(atomz[x])+"\n")
	f2.write("$end"+"\n"+"\n")
	f2.write("$comment"+"\n")
	for x in range (0,len(resname)):
		f2.write(str(atomnum[x])+"   "+resname[x]+"\n")
	f2.write("$end"+"\n")
	
	q += 1
	mult += 1
	apptemplate = f3.read()
	s1=apptemplate.format(charge=q, mult=mult, exch=exch, basis=basis, dielec=dielec)
	f2.write(s1)

	for x in range (0,len(resname)):
		f2.write(atomtype[x]+"   "+str(atomx[x])+"   "+str(atomy[x])+"   "+str(atomz[x])+"\n")
	f2.write("$end"+"\n"+"\n")

print("Done with " + outfile)
