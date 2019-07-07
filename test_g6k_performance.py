import sys
import time
import datetime
import subprocess
import json
import hashlib
import random
from statistics import mean, median
from test import *
from ssproblem import *

SAMPLE = 16
LOWER_BETA = 56
UPPER_BETA = 70

def main():
	res_obj = {}
	avg_running_times = []
	lattice_version = "Schnorr"
	instances_path = "instances/n_100/"
	lattices_path = instances_path + "N_16/"

	# 1. argument = "fpylll" or "pump n jump" or ...
	reduction_strategy = sys.argv[1]

	# we'll run run_g6k.py in parallel, so name the tmp filename different
	# in each run so that we avoid possible read/write conflicts
	
	samples = [ random.randint(1, 300) for i in range(SAMPLE) ]
	print("random samples: %s" % samples)

	for beta in range(LOWER_BETA, UPPER_BETA + 1):
		tmp_filename = "tmp" + str(beta) + reduction_strategy
		local_running_times = []
		for i in samples:
			dummy_options = " --bkz/pre_beta 2 --bkz/tours 1 --workers 1"
			alg_option = " --bkz/alg " + reduction_strategy
			file_in_option = " --file_in " + lattices_path + str(i) + "_" + lattice_version + "_lattice"
			# build eg. 54:55:1 -> that will run reduction only for beta = 54
			blocksizes_option = " --bkz/blocksizes " + str(beta) + ":" + str(beta + 1) + ":1"
			
			cmd_g6k = "../g6k/bkz_test_g6k.py 100" + dummy_options + alg_option + file_in_option + blocksizes_option + " --verbose"
			cmd_whole = cmd_g6k + " > " + tmp_filename
			print(cmd_whole)

			subprocess.call(cmd_whole, shell=True)

			# extract walltime
			f = open(tmp_filename, 'r')
			json_str = json.load(f)
			f.close()
			walltime = json_str["walltime"]

			local_running_times.append(walltime)

		local_avg = round(mean(local_running_times), 3)
		print("for beta %d the average running time was %f" % (beta, local_avg))
		avg_running_times.append((beta, local_avg))

		subprocess.call("rm " + tmp_filename, shell=True)
	
	print(avg_running_times)

if __name__ == "__main__":
    main()
