import subprocess
import os

#method to use
fxnal = 'wb97xd'
#basis set to use
basis = '6-31g*'

xyzdir = "rokss1xyz"
dtory = os.getcwd() + "/" + "SOCtddft@" + xyzdir + "-" + fxnal + "-TDA"
subprocess.call(["mkdir", dtory])

#generate qchem files from the xyz files
for i in os.listdir(os.getcwd() + '/' +xyzdir):
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

	qcfile.write("$molecule\n")
        #charge and multiplicity declaration
	qcfile.write("0 1\n")
	qcfile.writelines(coords + ["$end\n\n"])

	#$rem section
	qcfile.write("\n$rem\njobtype sp\nexchange " + fxnal + "\nbasis " + basis + "\ncis_n_roots 7\ncis_singlets true\ncis_triplets true\nrpa 0\nspin_orbit_couple true\n$end\n")

	qcfile.close()


	numcores = '1'

        subprocess.call(["sqthis -J tddft@" + xyzdir + "-" + fxnal + "_" + i + " -c " + numcores + " -t 240:00:00 ~/tests/qcrun -nt " + numcores + " " + dtory + "/" + i + "/" + i + ".in " + dtory + "/" + i + "/" + i + ".out"], shell = True)

