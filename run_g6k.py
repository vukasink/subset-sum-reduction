import sys
import time
import datetime
import subprocess
import json
import hashlib
from test import *
from ssproblem import *

FIRST_P = 1
LAST_P = 300

def main():
	print("***********************************************")
	print("CHECK FIRST_P and LAST_P parameters.")
	print("***********************************************")
	print("CHECK that right arguments have been passed.")
	print("***********************************************")

	time.sleep(5)

	res_obj = {}
	num_instances = LAST_P - FIRST_P + 1
	solved_instances = 0

	# 1. argument = "CA" or "Schnorr" or ...
	lattice_version = sys.argv[1]
	res_obj.update({"lattice_version": lattice_version})
	# 2. argument = "fpylll" or "pump n jump" or ...
	reduction_strategy = sys.argv[2]
	res_obj.update({"reduction_strategy": reduction_strategy})
	# 3. argument = N in lattice
	N = sys.argv[3]
	res_obj.update({"N": N})
	# 4. argument = problem dimension
	dimension = sys.argv[4]
	res_obj.update({"problem_dimension": dimension})
	res_obj.update({"num_instances": num_instances})
	# 5. argument = non-pruning blocksizes
	basic_blocksizes = sys.argv[5]
	res_obj.update({"non_pruning_betas": basic_blocksizes})
	# 5. argument = pruning blocksizes
	pruning_blocksizes = sys.argv[6]
	res_obj.update({"pruning_betas": pruning_blocksizes})
	
	total_running_time = 0
	# average running time per problem
	avg_running_time = 0
	# average running time per problem if we discard results
	# of X slowest/fastest tests
	opt_avg_running_time = 0

	instances_path = "instances/n_" + str(dimension) + "/"
	#print(instances_path)
	lattices_path = instances_path + "N_" + str(N) + "/"
	#print(lattices_path)

	res_obj.update({"results": []})

	tmp_filename = "g6k_run_tmp" + str(dimension) + str(N) + reduction_strategy
	
	# info_arr_1 = [ (instance_num, beta, time, slope) ]
	info_arr_1 = []

	for i in range(FIRST_P, LAST_P + 1):
		print("---------------------")
		print("current instance: %d" % i)
		dummy_options = " --bkz/pre_beta 2 --bkz/tours 1 --workers 1"
		alg_option = " --bkz/alg " + reduction_strategy
		file_in_option = " --file_in " + lattices_path + str(i) + "_" + lattice_version + "_lattice"
		solution_in = " --solution_in " + instances_path + str(i)
		basic_blocksizes_option = " --bkz/basic_blocksizes " + basic_blocksizes
		pruning_blocksizes_option = " --bkz/pruning_blocksizes " + pruning_blocksizes
		blocksizes_option = (basic_blocksizes_option if not basic_blocksizes == "0" else "") + (pruning_blocksizes_option if not pruning_blocksizes == "0" else "")
		#print(blocksizes_option)
		
		cmd_g6k = "../g6k/bkz_vkc.py 100" + dummy_options + alg_option + file_in_option + solution_in + blocksizes_option if reduction_strategy == "fpylll" else ""
		cmd_whole = cmd_g6k + " > " + tmp_filename
		#print(cmd_whole)

		subprocess.call(cmd_whole, shell=True)
		
		f = open(tmp_filename, 'r')
		json_str = json.load(f)
		f.close()
		
		info_arr_1.append((json_str["instance"], json_str["beta"], walltime, json_str["slope"]))

		res_obj_tmp = res_obj['results']
		res_obj_tmp.append(json_str)
		res_obj['results'] = res_obj_tmp

	res_obj.update({"total_running_time": total_running_time})
	avg_running_time = total_running_time / num_instances
	res_obj.update({"avg_runtime_per_problem": avg_running_time})
	# write final result to json file
	hash_obj = hashlib.sha1(cmd_g6k.encode())
	filename = "result_n_" + str(dimension) + "_N_" + str(N) + "_" + reduction_strategy + "_" + hash_obj.hexdigest()[0:6] + ".json" 
	f = open(filename, "w")
	f.write(json.dumps(res_obj, indent = 4, separators = (', ', ': ')))
	f.close()

if __name__ == "__main__":
    main()
