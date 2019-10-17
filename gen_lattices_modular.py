import os
from statistics import mean, median
from test import *
from ssproblem import *

NUM_INSTANCES = 300

def read_in_problems(dimension, first, last):
	tests = []
	path = "instances/n_" + str(dimension) + "/"
	for i in range(first, last + 1):
		test = Test(dimension)
		problem = SubsetSumProblem() # change this method
		f = open(path + str(i), 'r')

		# read in a_i's
		line = f.readline()
		line = line[1:-2]
		b = line.split(', ')
		A = [ int(elem) for elem in b ]
		problem.A = A
		problem.n = dimension
#		print(problem.A)

		# read in e_i's
		line = f.readline()
		line = line[1:-2]
		b = line.split(', ')
		E = [ int(elem) for elem in b ]
		problem.E = E
#		print(problem.E)

		# read in target sum
		line = f.readline()
		problem.s = int(line)
		# target sum is actually calculated mod 2^n
		problem.s = problem.s % 2**dimension

		# read in problem density
		line = f.readline()
		problem.d = float(line)
		test.ssproblem = problem
		tests.append(test)
		
	return tests

def main():
	N_array = [16]
#	dimensions = [ elem for elem in range(52, 102, 2) ]
	dimensions = [ elem for elem in range(52, 102, 2) ]
	
	for dimension in dimensions:
		print("generating lattices for dimension %d" % dimension)		
		tests = read_in_problems(dimension, 1, NUM_INSTANCES)		
		for N in N_array:
			mkdir = "instances/n_" + str(dimension) + "/modular_N_" + str(N)
			subprocess.call(['mkdir', mkdir])
	
		for N in N_array:
			for i in range(NUM_INSTANCES):
				instance = tests[i].ssproblem
		
				filename_path = "instances/n_" + str(dimension) + "/modular_N_" + str(N) + "/" + str(i + 1) + "_Schnorr_lattice"
				generate_input_file_fplll_modular(filename_path, instance, N)

if __name__ == "__main__":
    main()
