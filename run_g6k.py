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

"""
	global logfile

	tests = read_in_solutions(PROBLEMS_PATH, FIRST_P, LAST_P)

	N = sys.argv[1]
	LATTICES_PATH = PROBLEMS_PATH + "/N_" + str(N) + "/"

	n_succ = 0
	n_unsucc = NUM_INSTANCES
	i = STARTING_BLOCK_SIZE

	suite_start_time = datetime.datetime.now()
	logfile_name = "results/" + suite_start_time.strftime("%d%m%Y_%H:%M:%S") + ".log"

#	if (LOGTOFILE):
#		logfile = open(logfile_name, 'w')

	print("Test suite start at", suite_start_time.strftime("%d.%m.%Y, %H:%M:%S"), "\n")
	print("Subset Sum Problem dimension:", DIMENSION, "; Number of problem instances:", NUM_INSTANCES)
	print("set \'", PROBLEMS_PATH[-3:-1], "\' of instances ; ", "N = ", N, sep='')

	while (n_unsucc != 0):
		print("===============================================")
		print("BKZ block dimension:", i, "; #solved instances:", n_succ, "; #unsolved instances:", n_unsucc, "\n")
		for j in range(NUM_INSTANCES):
			if (not tests[j].success):
				print("running test on instance", j + 1, "...", end='')

				FILE_OUT_PATH = "out.txt"
				input_path = LATTICES_PATH + str(j + 1) + "_lattice"
				subprocess.call(['cp', input_path, '../fplll'])
			#	cmd = FPLLL_PATH + " -a bkz -b " + str(i) + " " + input_path + " > " + FILE_OUT_PATH
				cmd = FPLLL_PATH + " -a bkz -b " + str(i) + " -s ../fplll/strategies/default.json " + input_path + " > " + FILE_OUT_PATH

				start = time.time()
				subprocess.call(cmd, shell=True)
				end = time.time()
		
				total_time = round(end - start, 5)

				print(" time taken:", total_time, "secs", end='')
				
				succ = check_solution(FILE_OUT_PATH, tests[j].ssproblem.E, DIMENSION)

				if (succ == True):
					print(" ---> instance solved (problem dim. = ", tests[j].ssproblem.d, ")", sep='', end='')
					n_succ = n_succ + 1
					n_unsucc = n_unsucc - 1
					tests[j].bkz_block_dim = i
					tests[j].time = total_time
					tests[j].success = True
				print()
		
		i = i + 1
		print("\n===============================================")

	suite_end_time = datetime.datetime.now()
	
	print("\nTest suite ending at", suite_end_time.strftime("%d.%m.%Y, %H:%M:%S"), "\n")

	diagnostic_arr_1 = [] # will contain triplets (instance #, bkz_block_dim, time, problem dimension)
	diagnostic_arr_2 = []

	succ_time_total = 0

	max_block_dim = max([ test.bkz_block_dim for test in tests ])
	print("Statistics:")
	for i in range(STARTING_BLOCK_SIZE, max_block_dim + 1):
		succ_time_round_total = 0
		succ_sol_per_round = 0
		for j in range(NUM_INSTANCES):
			test = tests[j]
			if (test.bkz_block_dim == i):
				diagnostic_arr_1.append([i, j + 1, test.time, test.ssproblem.d])
				succ_time_total = succ_time_total + test.time
				succ_time_round_total = succ_time_round_total + test.time
				succ_sol_per_round = succ_sol_per_round + 1
		
		approx_time = 0
		if (succ_sol_per_round != 0):
			approx_time = round(succ_time_round_total / succ_sol_per_round, 5)
		print("BKZ block size:", i, "; instances solved:", succ_sol_per_round, "; approx. time per success: ", approx_time)
		
		diagnostic_arr_2.append([i, succ_sol_per_round, approx_time])

	# Total time measurement
	total_run_time = suite_end_time - suite_start_time
	print("\nTotal running time of reduction algorithm(s):", total_run_time)
	m, s = divmod(succ_time_total, 60)
	h, m = divmod(m, 60)
	ms = succ_time_total - int(succ_time_total)
	print("Total running time of reduction algorithm(s) where we found solution:", succ_time_total, "seconds")
	print(f'{h:d}:{m:02d}:{s:02d}.', end='')

	# Print out some diagnostic that can be useful for plotting
	print("\n")
	print("DIAGNOSTICS -> USE IT LATER")
	print(diagnostic_arr_1)
	print(diagnostic_arr_2)
"""

if __name__ == "__main__":
    main()
