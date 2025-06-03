#!/bin/bash
module load python


for i in *.bgf
do
	prefix=$(basename $i .bgf)
# input order - prefix exchange basis dielectric const. 
	python ~/JHcodes/IPSampling/bgftoIP.py ${prefix}.bgf M06-HF 6-31+G* 7.2

done
