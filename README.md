# IP-Sampling
A library of scripts to conduct cluster sampling from MD simulations in VMD and subsequent vertical IP calculations in Q-Chem.

# MD Requirements
An MD trajectory must be loaded into VMD with resname assignments for all atoms of interest. This can be done either by pre-loading a structure file with this information (e.g. .bgf file), or by manually assigning it via vmd's atomselect commands:

e.g. 

set sel [atomselect top "index 1 to 100"]

$sel set resname  SOL

Anion-TrajSave.tcl can then be run via Tk Console.
# IP Calculations
These scripts generate IP input files to be run with Q-Chem via the "Templates" directory.
Because the .tcl script generates individual .bgf cluster files, the QChem input files are generated individually with python scripts that are called via bash scripts.

To generate QChem inputs run bgftoqcin.sh in the directory containing Templates and the bgf files.

To analyze .qcouts after the Qchem runs, run Qcout-IP.sh.
