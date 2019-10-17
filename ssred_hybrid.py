import os
import sys
from subprocess import call
from statistics import mean, median
from random import shuffle
from math import sqrt
from itertools import combinations
from test import *
from ssproblem import *
from numpy import matmul
from numpy.linalg import solve, inv

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
		
		# read in problem density
		line = f.readline()
		problem.d = float(line)
		test.ssproblem = problem
		tests.append(test)
		
	return tests

# we aren't importing the function from parser.py
# as we need different (up to the row order) lattice
# in this case
def subset_sum_to_lattice_basis(ssproblem, N):
	B = []
	
	# generate first n columns of the matrix
	for i in range(ssproblem.n):
		b = []
		b.append(N * ssproblem.A[i])
		b.append(N)
		for j in range(ssproblem.n):
			if (j == i):
				b.append(2)
			else:
				b.append(0)
		b.append(0)
		B.append(b)
	last_col = [ 1 for i in range(ssproblem.n+3) ]
	last_col[0] = N * ssproblem.s
	last_col[1] = (ssproblem.n * N) // 2
	B.append(last_col)

	return B

# a bit different than the generate_input_file_fplll in parser.py 
def generate_input_file_fplll(filename, B):
	f = open(filename, 'w')
	f.write('[')
	for i in range(len(B)):
		f.write('[')
		for j in range(len(B[0])):
			f.write(" ")
			f.write(str(B[i][j]))
		f.write(']')
		if (i != len(B) - 1):
			f.write('\n')
	f.write(']')

# decompose B into suitable B_1
def make_B_1(B, n_2):
	row_dim = len(B[0])
	print("row dimension = %d" % row_dim)
	B_1_row_dim = row_dim - n_2
	n_1 = len(B) - n_2
	print("n_1 = %d" % n_1)
	B_1 = []
	for i in range(n_1):
		b = []
		for j in range(B_1_row_dim):
			b.append(B[i][j])
		B_1.append(b)
	return B_1

# decompose B into suitable B_2
def make_B_2(B, n_2):
	row_dim = len(B[0])
	print("row dimension = %d" % row_dim)
	B_2_row_dim = row_dim - n_2
	n_1 = len(B) - n_2
	print("n_1 = %d" % n_1)
	B_2 = []
	for i in range(n_2):
		b = []
		for j in range(B_2_row_dim):
			b.append(B[n_1 + i][j])
		B_2.append(b)
	return B_2

# decompose B into suitable B_4
def make_B_4(B, n_2):
	row_dim = len(B[0])
	print("row dimension = %d" % row_dim)
	B_4_row_dim = n_2
	n_1 = len(B) - n_2
	print("n_1 = %d" % n_1)
	B_4 = []
	for i in range(n_2):
		b = []
		for j in range(B_4_row_dim):
			b.append(B[n_1 + i][n_1 + 2 + j])
		B_4.append(b)
	return B_4

# parse G6K output into matrix basis
def parse_output(filename):
	B = []
	with open(filename, 'r') as openfileobject:
		for line in openfileobject:
			# get rid of '[' and ']'
			line = line[1:-3]
			# split string by whitespaces
			line = line.split()
			# cast str numbers into ints
			line = [int(elem) for elem in line]
			# print(line)
			B.append(line)
	return B

def dot_product(u, v):
	return sum([ u[i] * v[i] for i in range(len(u)) ])

def GSO(B):
#	print("***** entering GSO")
	B_p = []
	basis_dim = len(B)
	lattice_dim = len(B[0])
	print("basis dimension is %d, vector len is %d" % (basis_dim, lattice_dim))
	for i in range(basis_dim):
#		print("----")
#		print("-- i = %d" % i)
		b = B[i]
		for j in range(i):
#			print("j = %d" % j)
			if (i <= 0):	# in first loop
#				print("breaking, nothing to do here")
				break
			mu = dot_product(B[i], B_p[j]) / dot_product(B_p[j], B_p[j])
			subt = [ mu * elem for elem in B_p[j] ]
			b = [ b[i] - subt[i] for i in range(lattice_dim) ]
		B_p.append(b)
#	print("***** exiting GSO")
	return B_p

def nearest_plane_reduction(B, t):
	basis_dim = len(B)
	lattice_dim = len(B[0])
	B_GSO = GSO(B)
	tcp = t.copy()
	b = t.copy()
	# int(round(x))
	for i in range(basis_dim - 1, -1, -1):
		mu = int(round(dot_product(b, B_GSO[i]) / dot_product(B_GSO[i], B_GSO[i])))
		subt = [ mu * elem for elem in B[i] ]
		b = [ b[j] - subt[j] for j in range(lattice_dim) ]
	return [ tcp[i] - b[i] for i in range(lattice_dim) ]

def transpose(B):
	B_new = []
	for i in range(len(B[0])):
		b = []
		for vector in B:
			b.append(vector[i])
		B_new.append(b)
	return B_new

def main():
	# this can be made configurable via command line arguments
	# now it's static because it's WIP
	dimension = 50
	N = 16
	tests = read_in_problems(dimension, 5, 5)

	col_dim = dimension + 1

	# n_2 is length of (c_i, ..., c_{n + 1}), where i
	# is the 'separation parameter' mentioned in thesis.
	n_2 = 11

	min_norm = 100000
	max_norm = 0

	for test in tests:
		instance = test.ssproblem
		A = instance.A
		original_A = A.copy()

		# 1000 here is arbitrary number of permutations, for now!
		for i in range(1000):
			print("iteration (with new permutation) %d" % (i + 1))
			# permute A
			shuffle(A)
			instance.A = A
			print("A in this permutation iteration:")
			print(instance.A)
			B = subset_sum_to_lattice_basis(instance, N)
			"""
					| B_1 B_2 |	  | B_1 B_2 |
				B =	|		  | = |			|
					| B_3 B_4 |	  |  0  B_4 |
			
			- let us split B into B_1, B_2, B_4
			"""
			B_1 = make_B_1(B, n_2)
			B_2 = make_B_2(B, n_2)
			B_4 = make_B_4(B, n_2)

			print("Going to reduce B_1...")

			# blocksizes are arbitrary chosen here, for testing purposes
			generate_input_file_fplll("B_1_lattice", B_1)
			dummy_options = " --bkz/pre_beta 2 --bkz/tours 1 --workers 1"
			file_in_option = " --file_in B_1_lattice"
			blocksizes_option = " --bkz/basic_blocksizes 2:43:1 --bkz/pruning_blocksizes 43:52:1"				cmd_g6k = "../g6k/bkz_vkc.py 100" + dummy_options + file_in_option + blocksizes_option
			cmd_whole = cmd_g6k + " > tmp_hybrid_algorithm"
			subprocess.call(cmd_whole, shell=True)
			# beta-BKZ-reduced B_1
			B_1_reduced = parse_output("tmp_hybrid_algorithm")
		
			print("B_1 reduction done!")

			# transpose B_2 in order to use function matmul later
			B_2 = transpose(B_2)
			print("--- B2:")
			for elem in B_2:
				print(elem)
			print("--- end B2.")
			comb = list(range(n_2 - 1))
			
			cnt = 1
			for combination in combinations(comb, (n_2 - 1) // 2):
				s_2 = [ -1 if i in combination else 0 for i in range(n_2) ]
				s_2[len(s_2) - 1] = 1
				print("------------------------")
				print("interation %d" % cnt)
				cnt = cnt + 1
				# calculate target vector t (we call it v_2 here) = B_2 * s_2
				v_2 = matmul(B_2, s_2)
				v_2 = v_2.tolist()
				v_2 = [ -elem for elem in v_2 ]
				# run the Babai's Nearest Plane algorithm and save the output to bdd_sol
				bdd_sol = nearest_plane_reduction(B_1_reduced, v_2)

				diff = [ v_2[i] - bdd_sol[i] for i in range(0, len(v_2)) ]
				print("diff:")
				print(diff)
				diff_norm = sqrt(sum([ elem * elem for elem in diff ]))
				if (diff_norm < min_norm):
					min_norm = diff_norm
				if (diff_norm > max_norm):
					max_norm = diff_norm
				print("diff norm: %d" % int(diff_norm))
				# this below is currently there just for testing purposes, we are in
				# fact looking for even shorter norm (sqrt(i + 1))
				if (diff_norm < 60):
					print("SUCCESS! found vector with short norm")
	print("max norm encountered: %d" % int(max_norm))
	print("min norm encountered: %d" % int(min_norm))

if __name__ == "__main__":
    main()
