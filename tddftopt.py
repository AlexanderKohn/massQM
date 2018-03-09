import subprocess
import os

#method to use
fxnal = 'wb97xd'
#basis set to use
basis = '6-31g*'
#solvent dielectric constant
#solv = 'cyclohexane'

singStateOpt = "1"
dtory = os.getcwd() + "/" + "tddftOpt-s1-" + fxnal + "-RPA_froms0s1mecpIntermediatexyz"
subprocess.call(["mkdir", dtory])

#generate qchem files from the xyz files
for i in os.listdir(os.getcwd()+'/s0s1mecpIntermediatexyz'):
	if i.endswith('.xyz'):
		i = i[:-4]

	#make folders for every molecule
	subprocess.call(["mkdir", dtory + "/" + i])
	#copy the xyz file into the appropriate folder
	subprocess.call(["cp", "s0s1mecpIntermediatexyz/" + i + ".xyz", dtory + "/" + i + "/"])

	#modify the xyz files into the appropriate qchem file
	xyz = open(dtory + "/" + i + "/" + i + ".xyz", "r+")
	coords = xyz.readlines()[2:]
	xyz.close()


	qcfile = open(dtory + "/" + i + "/" + i + ".in", "w")
	#$rem section
        #start TDDFT section

	#$rem section
	qcfile.write("$rem\njobtype opt\nexchange " + fxnal + "\nbasis " + basis + "\ncis_n_roots " + "2" + "\ncis_singlets true\ncis_triplets false\nrpa 0\ncis_state_deriv " + singStateOpt + "\n$end\n\n")

	#$pcm solvent details
	#qcfile.write('$pcm\n$end\n\n$solvent\ndielectric ' + solvdtric + '\n$end\n\n')

	#qcfile.write('$smx\nsolvent ' + solv + '\ncharges chelpg\n$end\n\n')

	qcfile.write("$molecule\n")
        qcfile.write("0 1\n")
        qcfile.writelines(coords)
        qcfile.write("\n$end")
	qcfile.close()


	numcores = '4'

        subprocess.call(["sqthis -J tddftopts" + singStateOpt + "-"+fxnal+"_" + i + " -c " + numcores + " -t 72:00:00 qchem.latest -nt " + numcores + " " + dtory + "/" + i + "/" + i + ".in " + dtory + "/" + i + "/" + i + ".out"], shell = True)

	

