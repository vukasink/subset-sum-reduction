import sys
import time
import datetime
import json
import hashlib
import re
from subprocess import call
from multiprocessing import Manager, Process, JoinableQueue
from test import *
from ssproblem import *
# 58, [10, 16]
n_to_N = [ (50, [10, 14]), (52, [10, 14]), (54, [10, 16]), (56, [10, 16]), (58, [10, 16]),
			(60, [10, 14]), (62, [10, 16]), (64, [10, 16]), (66, [10, 16]), (68, [10, 16]),
			(70, [10, 16]), (72, [10, 16]), (74, [10, 16]), (76, [14, 16]), (78, [10, 16]),
			(80, [14, 16]), (82, [10, 16]), (84, [10, 16]), (86, [10, 16]), (88, [10, 16]),
			(90, [10, 16]), (92, [10, 16]), (94, [10, 16]), (96, [10, 16]), (98, [10, 16]),
			(100, [11, 16]) ]
FIRST_P = 1
LAST_P = 300

def solve_instance(q, task_count, results):
	while not q.empty():
		args = q.get()

		instance_num = args[0]
		n = args[1]
		N = args[2]
		instances_path = args[3]
		lattices_path = args[4]
		lattice_version = args[5]

#		time.sleep(1)
		tmp_filename = "g6k_run_tmp" + str(n) + str(N) + str(instance_num)
		dummy_options = " --bkz/pre_beta 2 --bkz/tours 1 --workers 1"
		file_in_option = " --file_in " + lattices_path + str(instance_num) + "_" + lattice_version + "_lattice"
		solution_in = " --solution_in " + instances_path + str(instance_num)
		blocksizes_option = " --bkz/basic_blocksizes 2.4.8.16.32 --bkz/pruning_blocksizes 33:110:1" 	
		cmd_g6k = "../g6k/bkz_ssred.py 100" + dummy_options + file_in_option + solution_in + blocksizes_option
		cmd_whole = cmd_g6k + " > " + tmp_filename
#		print(cmd_whole)
		subprocess.call(cmd_whole, shell=True)
	
#		time.sleep(1)
		f = open(tmp_filename, 'r')
		json_str = json.load(f)
		f.close()
		# clean up the temp file
		subprocess.call("rm " + tmp_filename, shell=True)
		
		# extract results
		walltime = json_str["walltime"]
		beta = json_str["beta"]
		slope = json_str["slope"]

#		total_running_time = total_running_time + walltime
		# running time of problems that were solved
#		if (beta > 0):
#			succ_running_time = succ_running_time + walltime
#			solved_instances = solved_instances + 1
#		info_arr_1.append((json_str["instance"], beta, walltime, json_str["slope"]))
		
		results.append(json_str)
		q.task_done()

def run_set(dimension, lattice_version):
	num_instances = LAST_P - FIRST_P + 1
	solved_instances = 0
	
	res_obj = {}
	res_obj.update({"lattice_version": lattice_version})
	res_obj.update({"problem_dimension": dimension})
	res_obj.update({"num_instances": num_instances})

	total_running_time = 0
	succ_running_time = 0
	# average running time per problem
	avg_running_time = 0

	res_obj.update({"results": []})

	N_array = [ elem[1] for elem in n_to_N if elem[0] == dimension]
	N_array = N_array[0]

	for N in N_array:
		# info_arr_1 = [ (instance_num, beta, time, slope) ]
		info_arr_1 = []

		with Manager() as manager:
			results = manager.list()
			q = JoinableQueue()
			instances_path = "instances/n_" + str(dimension) + "/"
			lattices_path = instances_path + "N_" + str(N) + "/"
			
			for i in range(FIRST_P, LAST_P + 1):
			# args are (problem instance num, n, 
				q.put((i, dimension, N, instances_path, lattices_path, lattice_version))
		
			# start the workers
			item_count = q.qsize()
			for i in range(3):
				worker = Process(target=solve_instance, args=(q, item_count, results))
				worker.start()

			# wait for all work to be done
			q.join()

			results = list(results)
			#print(results)

		# collect succ running time, avg_rungtime_per_succ_problem, total_running_time statistics
		for result in results:
			beta = result["beta"]
			walltime = result["walltime"]
			
			res_obj_tmp = res_obj['results']
			res_obj_tmp.append(result)
			res_obj['results'] = res_obj_tmp

			total_running_time = total_running_time + walltime
			# running time of problems that were solved
			if (beta > 0):
				succ_running_time = succ_running_time + walltime
				solved_instances = solved_instances + 1
				print("solved instance num %d" % solved_instances)
		res_obj.update({"succ_running_time": round(succ_running_time, 3)})
		avg_succ_running_time = round(succ_running_time / solved_instances, 3)
		res_obj.update({"avg_runtime_per_succ_problem": avg_succ_running_time})
		res_obj.update({"total_running_time": round(total_running_time, 3)})
		# write final result to json file
		hash_obj_name = str(dimension) + str(N)
		hash_obj = hashlib.sha1(hash_obj_name.encode())
		filename = "result_n_" + str(dimension) + "_N_" + str(N) + "_" +  hash_obj.hexdigest()[0:6] + ".json" 
		f = open(filename, "w")
		f.write(json.dumps(res_obj, indent = 4, separators = (', ', ': ')))
		f.close()

def main():
	# 1. argument = "CA" or "Schnorr" or ...
	lattice_version = sys.argv[1]
	# 2. argument = problem dimension
	dimension = sys.argv[2]
	dimensions = eval("range(%s)" % re.sub(":", ",", dimension))

	for n in dimensions:
		print("------------------------------")
		print("going to run tests on set n_" + str(n))
		print("------------------------------")
		run_set(n, lattice_version)
	print("------------------------------")
	print("end of program")
	print("------------------------------")

if __name__ == "__main__":
    main()
