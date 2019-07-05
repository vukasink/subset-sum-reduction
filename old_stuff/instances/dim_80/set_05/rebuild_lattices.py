#from ssproblem import *
#from test import *
import subprocess

NUM_INSTANCES = 50
DIMENSION = 80

def main():
	N_array = [11, 12, 20, 21, 23]
#	N_array = [9, 10, 13, 14, 15, 16, 17, 18, 19, 22]
#	prefix = "instances/set_10/"
	# generate 50 SSProblems of dim 80.
	for N in N_array:
		mkdir = "N_" + str(N)
		subprocess.call(['mkdir', mkdir])
	
	for i in range(NUM_INSTANCES):
		f = open(str(i + 1), 'r')
		line = f.readline()
		line = line[1:-2]
		
		arr = line.split(", ")
		arr = [ int(elem) for elem in arr ]

		f.readline()
		s = f.readline()
		s = int(s)
		f.close()

		for N in N_array:
			B = []

			# generate first n columns of the matrix
			for k in range(DIMENSION):
				b = []
				for j in range(DIMENSION):
					if (j == k):
						b.append(2)
					else:
						b.append(0)
				b.append(N * arr[k])
				b.append(0)
				b.append(N)
				B.append(b)
			last_col = [ 1 for inner in range(DIMENSION+3) ]
			last_col[DIMENSION] = N * s
			last_col[DIMENSION + 2] = (DIMENSION * N) // 2
			B.append(last_col)
			
			filename = "N_" + str(N) + "/" + str(i + 1) + "_lattice"
			wf = open(filename, 'w')
			wf.write('[')
			for k in range(DIMENSION + 1):
				wf.write('[')
				for j in range(DIMENSION + 3):
					wf.write(" ")
					wf.write(str(B[k][j]))
				wf.write(']')
				if (k != DIMENSION):
					wf.write('\n')
			wf.write(']')
			wf.close()


if __name__ == "__main__":
    main()
