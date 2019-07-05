import sys
import os
import time
import datetime
import subprocess
#from test import *
#from ssproblem import *

# from results/dim_*/set_* read in all test results (file by file)
#
# - first extract for each file N, total running time, and diagnostic arrays in the end

# N = 13
FIRST_P = 1
LAST_P = 50
NUM_INSTANCES = 50
DIMENSION = 80
STARTING_BLOCK_SIZE = 30
PROBLEMS_PATH = "instances/dim_" + str(DIMENSION) + "/set_21/"
FPLLL_PATH = "../fplll/fplll/fplll"

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
#	N = sys.argv[1]
	for test_log_path in os.listdir('.'):
		# skip any file that isn't (hopefully) a test result file
		if not ("set" in test_log_path):
			continue
		print(test_log_path)
		f = open(test_log_path, 'r')
		for line in f:
			# extract N
			number = 0
			if "of instances" in line:
				index = line.find('N = ')
				number = line[index + 3:-1]
			# extract running time
			timestr = ""
			if "algorithm(s):" in line:
				index = line.find("(s):")
				timestr = line[index + 5:-1]
				print(timestr)
				print(line)

if __name__ == "__main__":
    main()
