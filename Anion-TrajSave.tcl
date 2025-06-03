#==============================================================================================================
#This script tracks individual residue trajectories and every species within 3 Angstroms of them at each frame.
#To be used in VMD TkConsole
#Each frame saved as a BGF, If frame 0 is a structure file, make sure to delete it first. 
#Before running, identify the residue #s in your LAMMPS data file

#Author: John Holoubek
#==============================================================================================================

# Change the following to the save location and uncomment it.
#cd ~/Google\ Drive/research/DATADUMP/FramesfromVMD/

puts "What resname are we sampling around?:"
gets stdin resnm

puts "z is less than?:"
gets stdin zconst

puts "Sampling Radius?:"
gets stdin srad

#Find the tracked residues and save them
set tracksel [atomselect top "resname $resnm"]
set tracklist [$tracksel get residue]

set resstart [lindex $tracklist 0]
set resend [lindex $tracklist end]

# Get some inputs manual inputs for residue (Disabled)
#puts "Residue start:"
#gets stdin resstart
#puts "Residue end:"
#gets stdin resend

# Get some inputs manual inputs for Frames
puts "Start frame:"
gets stdin Framestart
puts "End frame:"
gets stdin Frameend

#For loop for residues
for {set rescount 0} {$rescount < [expr $resend-$resstart+1]} {incr rescount} {

#Find the current residue we are working on
set CurrentRes [expr $resstart+$rescount]

#Center the periodic simulation on your residue
pbc wrap -all -compound fragment -centersel "residue $CurrentRes" -center com	

	#For loop for Frames
	for {set i 0} {$i < [expr $Frameend-$Framestart+1]} {incr i} {

	#Find the current Frame we are working on
	set CurrentFrame [expr $Framestart+$i]
	
	#Make the atom selections
	set sel [atomselect top "residue $CurrentRes or (resname BTF and same fragment as within $srad of (residue $CurrentRes and z < $zconst)) or (resname DME and same fragment as within $srad of (residue $CurrentRes and z < $zconst)) or (resname Li and same fragment as within $srad of (residue $CurrentRes and z < $zconst))" frame $CurrentFrame] 
	$sel update
	#Set the file name for this frame	
	set fname "Res$CurrentRes.Frame$CurrentFrame.$srad.Ang"
	
	#Write the BGF for this frame
	animate write bgf $fname.bgf beg $CurrentFrame end $CurrentFrame waitfor all sel $sel
	animate write xyz $fname.xyz beg $CurrentFrame end $CurrentFrame waitfor all sel $sel
	}

}