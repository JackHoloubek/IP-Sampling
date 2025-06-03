#!/bin/bash
module load python


for i in *.qcout
do
	prefix=$(basename $i .qcout)
# input order - prefix exchange basis dielectric const. 
	python ~/JHcodes/IPSampling/IPSampler.py ${prefix}

done
