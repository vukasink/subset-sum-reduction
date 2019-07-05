import sys
import platform
import time
import datetime
import subprocess
#import matplotlib.pyplot as plot
from test import *
from ssproblem import *
#from parser import N

# N = 13
FIRST_P = 1
LAST_P = 50
NUM_INSTANCES = 50
DIMENSION = 80
STARTING_BLOCK_SIZE = 30
PROBLEMS_PATH = "instances/dim_80/set_11/"
#LATTICES_PATH = PROBLEMS_PATH + "/N_" + str(N) + "/"
FPLLL_PATH = "../fplll/fplll/fplll"
LOGTOFILE = True
logfile = 0

def read_in_solutions(path, first, last):
	tests = []
	for i in range(first, last + 1):
		test = Test(DIMENSION)
		problem = SubsetSumProblem() # change this method
		f = open(PROBLEMS_PATH + str(i), 'r')
	
		line = f.readline()
		line = f.readline()
		line = line[1:-2]

		b = line.split(', ')
		solution = [ int(elem) for elem in b ]
		problem.E = solution

	#	print(problem.E)

		# read problem density
		line = f.readline()
		line = f.readline()
		problem.d = float(line)

		test.ssproblem = problem

		tests.append(test)
		
	return tests

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

def log(*strings):
	global logfile
	print(strings)
	logfile.write("asd")
	

def main():
	global logfile
	
	print("XXXXXXXXXXXXXXXXx")
	print(platform.processor())
	print("XXXXXXXXXXXXXXXXx")

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
			if (not tests[j].success) and j != 17:
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

	########################
	##### DRAWING PLOT #####
	########################

"""

	min_block = min( [mem[0] for mem in diagnostic_arr_1] )
	min_time = min( [mem[2] for mem in diagnostic_arr_1] )
	max_block = max( [mem[0] for mem in diagnostic_arr_1] )
	max_time = max( [mem[2] for mem in diagnostic_arr_1] )

	# MAKE SURE DIMs on X axis are printed for every dimension (not 32, 34, 36, etc)
	# print minutes on Y axis?

	plot.figure(figsize=(10.8,7.2), dpi=300)
	
	plot.tick_params(axis='x', which='minor', bottom=False)
	plot.tick_params(axis='y', which='minor', length=3)
	plot.tick_params(axis='y', which='major', length=4.5)
	plot.tick_params(axis='x', which='major', length=4.5)
	
	plot.ylabel('Minutes')
	plot.xlabel('BKZ block size')
	
	plot.plot([mem[0] for mem in diagnostic_arr_1], [mem[2] / 60 for mem in diagnostic_arr_1], 'b.', label='individual running times per instance', markersize=2)
	plot.plot([mem[0] for mem in diagnostic_arr_2], [mem[2] / 60 for mem in diagnostic_arr_2], 'rx', markersize=8, label='average running time per dimension')
	
	plot.ylim(bottom = 1)
	
	plot.axis([min_block - 0.5, max_block + 0.5, 0, (max_time + 60) // 60])
	plot.xticks(range(min_block, max_block, 1))
	
	plot.legend()
	
	plot.savefig(suite_start_time.strftime("%d%m%Y_%H:%M:%S.png"), bbox_inches='tight')

"""

if __name__ == "__main__":
    main()
