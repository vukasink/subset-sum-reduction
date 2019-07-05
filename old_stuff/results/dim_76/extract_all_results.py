import sys
import os
import time
import datetime
import subprocess
import matplotlib.pyplot as plot
#from test import *
#from ssproblem import *

# from results/dim_*/set_* read in all test results (file by file)
#
# - first extract for each file N, total running time, and diagnostic arrays in the end

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
	
def trim(num):
	if (num[0] == "["):
		num = num[1:]
	if (num[0] == "["):
		num = num[1:]
	if (num[len(num) - 1] == "]"):
		num = num[:-1]
	if (num[len(num) - 1] == "]"):
		num = num[:-1]
	return num

def main():
	N = sys.argv[1]
	N = int(N)
	sets = ['set_01/', 'set_02/', 'set_03/', 'set_04/', 'set_05/']
	global_diag = []

	for set_path in sets:
		diag = []
		print("\nreading in from", set_path)
		for test_log_path in os.listdir(set_path):
			found_diag = 0

			# skip any file that isn't (hopefully) a test result file
			if not ("set" in test_log_path):
				continue
			
			print(test_log_path)
			
			f = open(set_path + test_log_path, 'r')
			
			for line in f:
				# extract N
				number = 0
				if "of instances" in line:
					index = line.find('N = ')
					number = line[index + 4:-1]
					number = int(number)
					if number != N:
						break

				if "DIAGNOSTICS" in line:
					found_diag = 1
					continue
				
				if (found_diag > 0):
					if (found_diag == 1):
						line = line[:-2]
						line = line.split(", ")
						line = [ trim(elem) for elem in line ]

						for i in range(0, len(line), 4):
							diag.append([ int(line[i]), int(line[i + 1]), float(line[i + 2]), float(line[i + 3]) ])

						found_diag = 2
					elif (found_diag == 2):
						line = line[:-2]
						found_diag = 0
		global_diag.append(diag)
	
	print("#################################")
	print("#################################")
	
	# we collected for each instance the following tuples:
	# [beta for which this problem was solved, instance number in the set, time used in successfull reduction, problem dimension]

	min_beta = 30
	max_1 = max([elem[0] for elem in global_diag[0]])
	max_2 = max([elem[0] for elem in global_diag[1]])
	max_3 = max([elem[0] for elem in global_diag[2]])
	max_4 = max([elem[0] for elem in global_diag[3]])
	max_5 = max([elem[0] for elem in global_diag[4]])
	max_beta = max([max_1, max_2, max_3, max_4, max_5])
	
	print(max_beta)

	solved_across_beta = [ 0 for beta in range(min_beta, max_beta + 1) ]
	average_den_across_beta = [ 0 for beta in range(min_beta, max_beta + 1) ]

	for diag in global_diag:
		for problem in diag:
			solved_across_beta[problem[0] - min_beta] = solved_across_beta[problem[0] - min_beta] + 1
			average_den_across_beta[problem[0] - min_beta] = average_den_across_beta[problem[0] - min_beta] + problem[3]

	average_den_across_beta = [ average_den_across_beta[i] / solved_across_beta[i] if solved_across_beta[i] != 0 else 0 for i in range(max_beta - min_beta + 1) ]
	print(solved_across_beta)
	print(average_den_across_beta)

	fig, ax1 = plot.subplots(figsize=(10.8, 7.2), dpi=300)

	ax1.set_xlabel('beta')
	ax1.set_ylabel('Problems solved', color='blue')
	
	major_yticks = list(range(10, max(solved_across_beta) + 10, 10))
	ax1.set_yticks([1] + major_yticks)
	ax1.set_ylim(bottom=0, top=max(solved_across_beta) + 2)
	ax1.set_yticks(range(1, max(solved_across_beta) + 1), minor=True)
	
	major_xticks = list(range(min_beta, max_beta + 5, 5))
	print("major xticks", major_xticks)
	ax1.set_xticks(major_xticks)
	ax1.set_xticks(range(min_beta, max_beta + 1), minor=True)
	
	ax1_plot = zip(list(range(min_beta, max_beta + 1)), solved_across_beta)
	ax1_plot = list(ax1_plot)
	ax1_plot = [ elem for elem in ax1_plot if elem[1] != 0 ]
	print(ax1_plot)
	ax1.plot([elem[0] for elem in ax1_plot], [elem[1] for elem in ax1_plot], 'bx', markersize=8)

#	plot.figure(figsize=(10.8,7.2), dpi=300)
#	plot.xlabel('beta')
#	plot.ylabel('Problems solved')

	ax2 = ax1.twinx()

	ax2.set_ylabel("Average density", color='red')
	ax2.set_ylim(bottom=0.5)
	ax2.plot(range(min_beta, max_beta + 1), average_den_across_beta, 'r+', markersize=8)

#	plot.plot(range(min_beta, max_beta + 1), solved_across_beta, 'b+', label='set 01', markersize=5)
	
#	plot.xticks(range(min_beta, max_beta + 1, 1))
	
#	plot.legend(prop={'size' : 8})
	plot.savefig("example", bbox_inches='tight')

if __name__ == "__main__":
    main()
