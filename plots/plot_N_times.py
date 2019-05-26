import matplotlib.pyplot as plot
import datetime
import time

def main():

	N = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ] #23]
	set_01_values = [ 19.555, 21.221, 24.266, 21.959, 28.865, 23.042, 23.332, 25.857, 25.145, 18.633, 22.668, 24.458, 22.601, 20.723 ]
	set_02_values = [ 9.227, 8.039, 7.705, 6.419, 8.612, 7.351, 7.874, 10.655, 8.2, 7.685, 7.276, 7.443, 8.222, 9.8 ]
	set_04_values = [ 17.602, 14.855, 13.992, 13.183, 13.673, 11.606, 15.581, 12.455, 16.558, 14.319, 16.296, 12.45, 10.462, 11.616 ]
	set_05_values = [ 11.016, 10.214, 10.296, 8.124, 8.738, 11.5, 9.580, 10.401, 8.457, 10.795, 8.761, 9.786, 8.037, 10.155 ]

	average = [ (set_01_values[i] + set_02_values[i] + set_04_values[i] + set_05_values[i]) / 4 for i in range(14) ]

	N_average = zip(N, average)
	min_point = [ elem for elem in N_average if elem[1] == min(average)]
	print(min_point)
	print(min(average))

#	min_block = min( [mem[0] for mem in diagnostic_arr_1] )
#	min_time = min( [mem[2] for mem in diagnostic_arr_1] )
#	max_block = max( [mem[0] for mem in diagnostic_arr_1] )
#	max_time = max( [mem[2] for mem in diagnostic_arr_1] )

	plot.figure(figsize=(10.8,7.2), dpi=300)
	
#	plot.tick_params(axis='x', which='minor', bottom=False)
#	plot.tick_params(axis='y', which='minor', length=3)
#	plot.tick_params(axis='y', which='major', length=4.5)
#	plot.tick_params(axis='x', which='major', length=4.5)
#	plot.minorticks_on()
	plot.xlabel('N')
	plot.ylabel('Minutes')
	
	plot.plot(N, set_01_values, 'b', label='set 01', markersize=3)
	plot.plot(N, set_02_values, 'r', markersize=3, label='set 02')
	plot.plot(N, set_04_values, 'g', markersize=3, label='set 04')
	plot.plot(N, set_05_values, 'y', markersize=3, label='set 05')
	plot.plot(N, average, 'm', linestyle=":", linewidth=2.5, label='average over all sets')
	
#	plot.ylim(bottom = 1)
#	plot.axis([min_block - 0.5, max_block + 0.5, 0, (max_time + 60) // 60])
	plot.xticks(range(min(N), max(N) + 1, 1))
	
	plot.legend()
	plot.savefig('example.png', bbox_inches='tight')

if __name__ == "__main__":
    main()
