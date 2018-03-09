import subprocess
import os

#method to use
fxnal = 'wb97xd'
#basis set to use
basis = '6-31G*'

dtory = "s0@s0-" + fxnal


subprocess.call(["mkdir", dtory])

#generate qchem files from the xyz files
for i in os.listdir(os.getcwd()+'/s0xyz'):
	if i.endswith('.xyz'):
        	i = i[:-4]

	#make folders for every molecule
	subprocess.call(["mkdir", dtory + "/" + i])
	#copy the xyz file into the appropriate folder
	subprocess.call(["cp", "s0xyz/" + i + ".xyz", dtory + "/" + i + "/"])

	#modify the xyz files into the appropriate qchem file
	xyz = open(dtory + "/" + i + "/" + i + ".xyz", "r+")
	coords = xyz.readlines()[2:]
	xyz.close()


	qcfile = open(dtory + "/" + i + "/" + i + ".in", "w")
	#$rem section
	qcfile.write("$rem\njobtype opt\nexchange " + fxnal + "\nbasis " + basis + "\n$end\n\n")
	#$pcm solvent details
	#qcfile.write('$pcm\n$end\n\n$solvent\ndielectric ' + solvdtric + '\n$end\n\n')
	#qcfile.write('\n$smx\nsolvent ' + solv + '\n$end\n\n')


	qcfile.write("$molecule\n")
#charge and multiplicity declaration
	qcfile.write("0 1\n")
	qcfile.writelines(coords + ["$end\n\n"])
	qcfile.close()

	numcores = '2'

        subprocess.call(["sqthis -J s0@s0_" + i + " -c " + numcores + " -t 72:00:00 qchem.latest -nt " + numcores + " " + dtory + "/" + i + "/" + i + ".in " + dtory + "/" + i + "/" + i + ".out"], shell = True)

	




