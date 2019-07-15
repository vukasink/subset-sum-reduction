import os
import json
import datetime
import matplotlib.pyplot as plot
from statistics import mean, median
from test import *
from ssproblem import *

NUM_INSTANCES = 300
DIMENSION = 74
PROBLEMS_PATH = "instances/n_" + str(DIMENSION) + "/"
RESULTS_PATH = "results/not_finished/"
PRUNING_STRATEGY = "2:33:1"

def read_in_problems(path, first, last):
	tests = []
	for i in range(first, last + 1):
		test = Test(DIMENSION)
		problem = SubsetSumProblem() # change this method
		f = open(PROBLEMS_PATH + str(i), 'r')

		# read in a_i's
		line = f.readline()
		line = line[1:-2]
		b = line.split(', ')
		A = [ int(elem) for elem in b ]
		problem.A = A
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
		
		# read in problem density
		line = f.readline()
		problem.d = float(line)

		test.ssproblem = problem
		tests.append(test)
		
	return tests
	
def read_in_results():
	for filename in os.listdir(RESULTS_PATH):
		solved_instances = 0
		if filename.endswith(".json"):

			f = open(RESULTS_PATH + filename, "r")
			json_obj = json.load(f)
	
			dimension = int(json_obj["problem_dimension"])
			if (not dimension == DIMENSION):
				continue
			if (not json_obj["non_pruning_betas"] == PRUNING_STRATEGY):
				continue

			print("******************************************")
			print("Reading in results of the problems with dimension %d (N = %d) and non pruning strategy %s" % (dimension, int(json_obj["N"]), PRUNING_STRATEGY))
			print("******************************************\n")
			
			N = json_obj["N"]
			num_instances = json_obj["num_instances"]
			total_running_time = json_obj["total_running_time"]
			succ_running_time = json_obj["succ_running_time"]
			avg_runtime_per_succ_problem = json_obj["avg_runtime_per_succ_problem"]
			# results should be an array
			results = json_obj["results"]
			all_results = []
			succ_results = []
	
			# non-zero
			min_beta = 1000
			max_beta = 1

			for elem in results:
				instance_num = elem["instance"]
				walltime = elem["walltime"]
				slope = elem["slope"]
				beta = elem["beta"]
				all_results.append((instance_num, walltime, beta, slope))
				if (beta != 0):
					solved_instances = solved_instances + 1
					succ_results.append((instance_num, walltime, beta, slope))
					if (beta < min_beta):
						min_beta = beta
					if (beta > max_beta):
						max_beta = beta

			sorted_walltime_succ = sorted(succ_results, key = lambda x: x[1], reverse = True)
			return all_results, sorted_walltime_succ
	return [], []

def square(num):
	return num * num

def main():
	tests = read_in_problems(PROBLEMS_PATH, 1, NUM_INSTANCES)
	all_results, succ_results = read_in_results()

	for i in range(NUM_INSTANCES):
		tmp = all_results[i]
		tmp = tmp + (tests[tmp[0] - 1].ssproblem.d, )
		all_results[i] = tmp
		for j in range(len(succ_results)):
			if (succ_results[j][0] - 1 == i):
				tmp_succ = succ_results[j]
				tmp_succ = tmp_succ + (tests[tmp[0] - 1].ssproblem.d, )
				succ_results[j] = tmp_succ

	unsolved_probs = set(all_results).symmetric_difference(set(succ_results))
	print("Unsolved problems")
	for elem in unsolved_probs:
		print(elem)
	
	print("\nFirst 10 problems that took most time")
	for i in range(15):
		print(succ_results[i])
	
	sum_avg_A_total = 0
	sum_avg_A_contributing = 0
	averages = []

	for i in range(NUM_INSTANCES):
		A_total = 0
		avg_A = 0
		A_contributing = 0
		avg_A_contributing = 0

		problem = tests[i].ssproblem

		for j in range(DIMENSION):
			A_total = A_total + problem.A[j]
			A_contributing = A_contributing + (problem.A[j] if problem.E[j] == 1 else 0)
	
		avg_A = A_total // DIMENSION
		avg_A_contributing = A_contributing // (DIMENSION // 2)

		averages.append([avg_A, avg_A_contributing])
		
		sum_avg_A_total = sum_avg_A_total + avg_A
		sum_avg_A_contributing = sum_avg_A_contributing + avg_A_contributing

	avg_avg_A_total = sum_avg_A_total // NUM_INSTANCES
	avg_avg_A_contributing = sum_avg_A_contributing // NUM_INSTANCES

#	print("Average sum of a_i's over all problems:              %40d" % avg_avg_A_total)
#	print("Average sum of a_i's contributing over all problems: %40d\n" % avg_avg_A_contributing)

	diagnostic = []
	diagnostic_contr = []
	diagnostic_parity = []

	for i in range(NUM_INSTANCES):
		problem = tests[i].ssproblem

		A_contr = [ problem.A[k] for k in range(DIMENSION) if problem.E[k] == 1 ]
		
		# count the number of (contributing) even/odd a_i's
		even_elems = len([elem for elem in problem.A if elem % 2 == 0])
		odd_elems = len(problem.A) - even_elems
		even_elems_contr = len([elem for elem in A_contr if elem % 2 == 0])
		odd_elems_contr = len(A_contr) - even_elems_contr
		diagnostic_parity.append([i + 1, even_elems, odd_elems, even_elems_contr, odd_elems_contr])
#		print(diagnostic_parity[i], "; ", even_elems_contr, "; ", odd_elems_contr, ": ", len(A_contr))

		# Statistic over whole A
		A_mean = mean(problem.A)
		A_median = median(problem.A)

		absolute_mean_deviances = [ abs(A_mean - a_i) for a_i in problem.A ]
		absolute_median_deviances = [ abs(A_median - a_i) for a_i in problem.A ]
		
		max_absolute_mean_deviation = max(absolute_mean_deviances)
		max_absolute_median_deviation = max(absolute_median_deviances)
		min_absolute_mean_deviation = min(absolute_mean_deviances)
		min_absolute_median_deviation = min(absolute_median_deviances)
		
		mean_absolute_deviation = mean(absolute_mean_deviances)
		median_absolute_deviation = median(absolute_median_deviances)

		# Statistic over a_i's that contribute to the target sum
		A_contr_mean = mean(A_contr)
		A_contr_median = median(A_contr)
		
		absolute_mean_deviances_contr = [ abs(A_contr_mean - a_i) for a_i in A_contr ]
		absolute_median_deviances_contr = [ abs(A_contr_median - a_i) for a_i in A_contr ]
		
		max_absolute_mean_deviation_contr = max(absolute_mean_deviances_contr)
		max_absolute_median_deviation_contr = max(absolute_median_deviances_contr)
		min_absolute_mean_deviation_contr = min(absolute_mean_deviances_contr)
		min_absolute_median_deviation_contr = min(absolute_median_deviances_contr)

		mean_absolute_deviation_contr = mean(absolute_mean_deviances_contr)
		median_absolute_deviation_contr = median(absolute_median_deviances_contr)

		# tuples in diagnostic array have following elements on following places:
		# index 0.  -> problem instance number
		# *** next 6 statistical values/measurements are taken over whole A
		# index 1.	-> maximal absolute mean deviation
		# index 2.	-> minimal absolute mean deviation
		# index 3.	-> maximal absolute median deviation
		# index 4.	-> minimal absolute median deviation
		# index 5.	-> mean absolute deviation
		# index 6.	-> median absolute deviation
		# *** next 6 statistical values/measurements are taken over a_i's that contribute to the target sum
		# index 7.	-> maximal absolute mean deviation
		# index 8.	-> minimal absolute mean deviation
		# index 9.	-> maximal absolute median deviation
		# index 10.	-> minimal absolute median deviation
		# index 11.	-> mean absolute deviation
		# index 12.	-> median absolute deviation
		# ***
		# index 13. -> maximal a_i
		diagnostic.append([i,
		max_absolute_mean_deviation, min_absolute_mean_deviation,
		max_absolute_median_deviation, min_absolute_median_deviation,
		mean_absolute_deviation, median_absolute_deviation,
		max_absolute_mean_deviation_contr, min_absolute_mean_deviation_contr,
		max_absolute_median_deviation_contr, min_absolute_median_deviation_contr,
		mean_absolute_deviation_contr, median_absolute_deviation_contr,
		max(problem.A), problem.d])

	# sorted without any addition parameters sorts in _ascending_ order

	print("\n******************************************")
	print("sorted by mean absolute deviation")
	print("******************************************\n")

	sorted_MAD = sorted(diagnostic, key = lambda x: x[5])
#	for i in range(NUM_INSTANCES):
#		print("problem = %2d; max_absolute_deviation %40d; mean_absolute_deviation_contr %40d" % (sorted_MAD[i][0] + 1, sorted_MAD[i][1], sorted_MAD[i][11]))
#		print("----")

	sorted_max_abs_mean = sorted(diagnostic, key = lambda x: x[1])
	sorted_min_abs_mean = sorted(diagnostic, key = lambda x: x[2])
	sorted_max_abs_median = sorted(diagnostic, key = lambda x: x[3])

#	print("\n***************")
#	print("sorted by mean absolute deviation contributing")
#	print("***************\n")

	sorted_MAD_contr = sorted(diagnostic, key = lambda x: x[11])

	sorted_max_abs_mean_contr = sorted(diagnostic, key = lambda x: x[7])
	sorted_min_abs_mean_contr = sorted(diagnostic, key = lambda x: x[8])
	sorted_max_abs_median_contr = sorted(diagnostic, key = lambda x: x[9])

#	for i in range(NUM_INSTANCES):
#		print("problem = %2d; mean_absolute_deviation %40d; mean_absolute_deviation_contr %40d" % (sorted_MAD_contr[i][0] + 1, sorted_MAD_contr[i][5], sorted_MAD_contr[i][11]))
#		print("----")

	sorted_max_A = sorted(diagnostic, key = lambda x: x[13])

	sorted_density = sorted(diagnostic, key = lambda x: x[14])

	

	print("MeanAD | MeanAD c. | MXaMean | MNaMean | MXaMed | MXaMean c. | MNaMean c. | MXaMed c. | MXa_i |")
	for i in range(NUM_INSTANCES):
		print("%4d   |  %4d     | %4d    |  %4d   |  %4d  |  %5d     |  %5d     |  %5d    | %4d  |" % (sorted_MAD[i][0] + 1,
		sorted_MAD_contr[i][0] + 1, sorted_max_abs_mean[i][0] + 1, sorted_min_abs_mean[i][0] + 1,
		sorted_max_abs_median[i][0] + 1, sorted_max_abs_mean_contr[i][0] + 1, sorted_min_abs_mean_contr[i][0] + 1,
		sorted_max_abs_median_contr[i][0] + 1, sorted_max_A[i][0] + 1))

	print("\nsorted by density")
	for i in range(NUM_INSTANCES):
		print("%5d" % (sorted_density[i][0] + 1))

if __name__ == "__main__":
    main()
