# IP-Sampling
A library of scripts to conduct cluster sampling from MD simulations in VMD and subsequent vertical IP calculations in Q-Chem.

# MD Requirements
An MD trajectory must be loaded into VMD with resname assignments for all atoms of interest. This can be done either by pre-loading a structure file with this information (e.g. .bgf file), or by manually assigning it via vmd's atomselect commands:

e.g. 
set sel [atomselect top "index 1 to 100"]
$sel set resname  SOL
