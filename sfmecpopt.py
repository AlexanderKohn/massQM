import subprocess
import os

#method to use
fxnal = 'wb97xd'
#basis set to use
basis = '6-31g*'
#solvent dielectric constant
#solv = 'cyclohexane'

state1 = "[0,1]"
state2 = "[0,2]"
name = "s0s1sf"
energyTol = "100" #In 10^-8 Hartrees
xyzdir = "s0s1mecpIntermediatexyz"
dtory = os.getcwd() + "/" + "mecp-" + name + "-" + fxnal + "_from" + xyzdir
subprocess.call(["mkdir", dtory])

maxState = str(max(int(state1[3]), int(state2[3]))*2)
#generate qchem files from the xyz files
for i in os.listdir(os.getcwd()+'/' + xyzdir):
	if i.endswith('.xyz'):
		i = i[:-4]

	#make folders for every molecule
	subprocess.call(["mkdir", dtory + "/" + i])
	#copy the xyz file into the appropriate folder
	subprocess.call(["cp", xyzdir + "/" + i + ".xyz", dtory + "/" + i + "/"])

	#modify the xyz files into the appropriate qchem file
	xyz = open(dtory + "/" + i + "/" + i + ".xyz", "r+")
	coords = xyz.readlines()[2:]
	xyz.close()


	qcfile = open(dtory + "/" + i + "/" + i + ".in", "w")
	#$rem section
        #start TDDFT section

	#$rem section
	qcfile.write("$rem\njobtype opt\ngeom_opt_tol_energy " + energyTol + "\nmecp_opt true\nmecp_methods penalty_function\nmecp_state1 " + state1 + "\nmecp_state2 " + state2 + "\nexchange " + fxnal + "\nbasis " + basis + "\ncis_n_roots " + maxState + "\nspin_flip true\nunrestricted true\n$end\n\n")

	#$pcm solvent details
	#qcfile.write('$pcm\n$end\n\n$solvent\ndielectric ' + solvdtric + '\n$end\n\n')

	#qcfile.write('$smx\nsolvent ' + solv + '\ncharges chelpg\n$end\n\n')

	qcfile.write("$molecule\n")
        qcfile.write("0 3\n")
        qcfile.writelines(coords)
        qcfile.write("\n$end")
	qcfile.close()


	numcores = '4'

        subprocess.call(["sqthis -J sfmecp" + name + fxnal + i + " -c " + numcores + " -t 240:00:00 qchem.latest -nt " + numcores + " " + dtory + "/" + i + "/" + i + ".in " + dtory + "/" + i + "/" + i + ".out"], shell = True)

	

