import subprocess
import os

#method to use
fxnal = 'wb97xd'
#basis set to use
basis = '6-31g*'
#solvent dielectric constant
#solv = 'cyclohexane'

dtory = os.getcwd() + "/" + "tddft@roksgeom-" + fxnal + "-froms1"
subprocess.call(["mkdir", dtory])

#generate qchem files from the xyz files
for i in os.listdir(os.getcwd()+'/s1xyz'):
	if i.endswith('.xyz'):
		i = i[:-4]

	#make folders for every molecule
	subprocess.call(["mkdir", dtory + "/" + i])
	#copy the xyz file into the appropriate folder
	subprocess.call(["cp", "s1xyz/" + i + ".xyz", dtory + "/" + i + "/"])

	#modify the xyz files into the appropriate qchem file
	xyz = open(dtory + "/" + i + "/" + i + ".xyz", "r+")
	coords = xyz.readlines()[2:]
        z.close()


	qcfile = open(dtory + "/" + i + "/" + i + ".in", "w")
	#$rem section
	qcfile.write("$rem\njobtype sp\nmethod " + fxnal + "\nbasis " + basis + "\nmax_scf_cycles 400\n$end\n\n")

	#$pcm solvent details
	#qcfile.write('$pcm\n$end\n\n$solvent\ndielectric ' + solvdtric + '\n$end\n\n')
	#qcfile.write('$smx\nsolvent ' + solv + '\n$end\n\n')
	#qcfile.write('$xc_functional\nX HF 1.0\nX BNL 0.9\nC LYP 1.0\n$end\n\n')



	qcfile.write("$molecule\n")
        #charge and multiplicity declaration
	qcfile.write("0 1\n")
	qcfile.writelines(coords + ["$end\n\n@@@\n\n"])

        #ROKS Optimization
	qcfile.write("$rem\njobtype opt\nmethod " + fxnal + "\nbasis " + basis + "\nroks 1\nunrestricted false\nmax_scf_cycles 400\nsymmetry false\nsym_ignore true\nscf_guess read\n$end\n\n")

	#qcfile.write('$smx\nsolvent ' + solv + '\n$end\n\n')

        qcfile.write("$molecule\nREAD\n$end\n")

        #start TDDFT section

	#$rem section
	qcfile.write("@@@\n\n$rem\njobtype sp\nexchange " + fxnal + "\nbasis " + basis + "\ncis_n_roots 10\ncis_singlets true\ncis_triplets true\nrpa 0\n$end\n\n")

	#$pcm solvent details
	#qcfile.write('$pcm\n$end\n\n$solvent\ndielectric ' + solvdtric + '\n$end\n\n')

	#qcfile.write('$smx\nsolvent ' + solv + '\n$end\n\n')

	qcfile.write("$molecule\nREAD\n$end\n\n")
	qcfile.close()


	numcores = '4'

        subprocess.call(["sqthis -J roks@roks-"+fxnal+"_" + i + " -c " + numcores + " -t 240:00:00 qchem.latest -nt " + numcores + " " + dtory + "/" + i + "/" + i + ".in " + dtory + "/" + i + "/" + i + ".out"], shell = True)

	

