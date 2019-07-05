import sys
import time
import datetime
import subprocess
from test import *
from ssproblem import *

FIRST_P = 1
LAST_P = 300
NUM_INSTANCES = 300

# n - dimension
def check_solution(out_file_path, solution, n):
	f = open(out_file_path, 'r')
	line = f.readline()

	line = line[2:-3]
	b = line.split(' ')
	b = [ int(b[i]) for i in range(n + 3) ]
#	print(b)

	if (b[n] != 0 or abs(b[n + 1]) != 1 or b[n + 2] != 0):
		return False

	for i in range(n):
		b_i = abs(b[i] - b[n + 1]) // 2
		if (b_i != solution[i]):
			return False
	
	return True

def main():
	# 1. argument = "CA" or "Schnorr" or ...
	lattice_version = sys.argv[1]
	# 2. argument = "fpylll" or "pump n jump" or ...
	reduction_strategy = sys.argv[2]
	# 3. argument = problem dimension
	dimension = sys.argv[3]
	# 4. argument = N in lattice
	N = sys.argv[4]

	instances_path = "~/ssred/instances/n_" + str(dimension) + "/"
	print(instances_path)
	lattices_path = instances_path + "N_" + str(N) + "/"
	print(lattices_path)
	for i in range(FIRST_P, LAST_P + 1):
		dummy_options = "--bkz/pre_beta 2 --bkz/tours 1 --workers 1 --verbose"
		alg_option = "--bkz/alg fpylll"
		cmd = "bkz_vkc.py 100 --bkz/betas 2:79:1 " + dummy_options + alg_option

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
#	print(f'{h:d}:{m:02d}:{s:02d}.', end='')

	# Print out some diagnostic that can be useful for plotting
	print("\n")
	print("DIAGNOSTICS -> USE IT LATER")
	print(diagnostic_arr_1)
	print(diagnostic_arr_2)
"""

if __name__ == "__main__":
    main()
