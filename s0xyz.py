import subprocess
import os

dtory = "mecp-s0s1-wb97xd-TDA-froms1xyz"
for i in os.listdir(os.getcwd() + "/" + dtory):

	subprocess.call(["q2x_deprecated " + dtory + "/" + i + "/" + i + ".out > " + "s0s1mecpIntermediatexyz/" + i + ".xyz"], shell=True)


