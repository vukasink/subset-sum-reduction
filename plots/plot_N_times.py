import matplotlib.pyplot as plot
import datetime
import time

# filename = "dim_76_category_I_N_times"
# filename = "dim_80_category_I_N_times"
filename = "dim_84_category_I_N_times"

def main():
	extra_data_file = open(filename + ".txt", 'w')

	# dim 76
#	N = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
	set_01 = [9.8882, 8.6509, 11.327, 10.5779, 11.1388, 9.5217, 9.8552, 8.2136, 9.4171, 9.6277, 11.1909, 9.191, 12.2092, 9.1859]
#	set_02 = [3.4715, 4.3917, 4.5149, 3.7408, 3.6614, 3.6119, 3.9588, 3.552, 4.1622, 4.5842, 4.277, 3.6436, 3.5759, 3.9793]
#	set_03 = [13.7593, 15.4044, 13.6469, 13.7319, 12.8171, 12.9912, 13.7214, 12.7198, 13.2733, 13.3311, 13.2514, 13.1409, 12.9491, 13.2768]
#	set_04 = [12.3763, 14.0702, 15.7605, 13.7352, 15.2879, 15.7396, 15.826, 17.5281, 15.081, 15.3002, 15.5682, 17.2343, 13.2672, 14.9917]
#	set_05 = [11.1428, 22.1304, 11.7541, 12.4856, 11.3756, 10.7919, 11.3174, 11.2224, 11.5619, 13.6069, 11.1156, 9.6878, 12.8386, 10.8921]

	# dim 80
#	N = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
#	set_01 = [19.4056, 23.1249, 24.3324, 21.9932, 28.3492, 22.3092, 23.0785, 23.873, 24.4833, 18.8911, 22.5357, 24.4578, 22.7317, 20.9434, 27.4013]
#	set_02 = [9.227, 8.0387, 7.7055, 6.4196, 8.6122, 7.351, 7.8736, 10.6553, 8.2003, 7.6846, 7.2763, 7.4428, 8.2225, 9.7998, 8.4441]
#	set_03 = [6.3744, 7.8425, 8.0507, 8.5565, 8.2948, 5.4752, 7.7663, 6.1721, 7.7422, 8.7474, 6.5846, 7.7074, 7.1387, 7.2677, 9.8198]
#	set_04 = [17.6022, 14.8547, 13.9921, 13.1832, 13.6735, 11.6062, 15.5811, 12.4548, 16.5583, 14.3195, 16.2961, 12.4497, 10.4623, 11.6163, 17.5554]
#	set_05 = [11.0158, 10.214, 10.2962, 8.1236, 8.7379, 11.4998, 9.5801, 10.4015, 8.4571, 10.7954, 8.7615, 9.7862, 10.0622, 8.0367, 10.1552]

	# dim 84
	N = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
	set_01 = [34.7333, 41.1756, 39.447, 41.1358, 39.6021, 40.6545, 38.174, 40.8857, 38.2987, 46.9405, 36.017, 36.4766, 43.0775, 39.2167, 35.7969]
	set_02 = [36.0811, 31.1553, 43.4605, 36.0065, 45.8371, 43.2677, 45.9182, 31.2268, 31.0212, 52.0792, 37.8489, 30.9864, 39.1889, 33.1496, 32.6138]
	set_03 = [28.2848, 22.7672, 28.9603, 20.5558, 22.7856, 22.9572, 25.3786, 21.7238, 23.2859, 24.6375, 23.2738, 24.7262, 20.0135, 25.1433, 24.9014]

#	average = [ round((set_01[i] + set_02[i] + set_03[i] + set_04[i] + set_05[i]) / 5, 4) for i in range(len(N)) ]
	average = [ round((set_01[i] + set_02[i] + set_03[i]) / 3, 4) for i in range(len(N)) ]

	N_average = zip(N, average)
	N_average_sorted = sorted(N_average, key = lambda x: x[1])
	
	print(N_average_sorted)
	extra_data_file.write(str(N_average_sorted))

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
	
	plot.plot(N, set_01, 'b', label='set 01', markersize=3)
	plot.plot(N, set_02, 'r', markersize=3, label='set 02')
	plot.plot(N, set_03, 'c', markersize=3, label='set 03')
#	plot.plot(N, set_04, 'g', markersize=3, label='set 04')
#	plot.plot(N, set_05, 'y', markersize=3, label='set 05')
	plot.plot(N, average, 'm', linestyle=":", linewidth=2.5, label='average over all sets')
	
#	plot.ylim(bottom = 1)
#	plot.axis([min_block - 0.5, max_block + 0.5, 0, (max_time + 60) // 60])
	plot.xticks(range(min(N), max(N) + 1, 1))
	
	plot.legend(prop={'size' : 8})
	plot.savefig(filename, bbox_inches='tight')

	extra_data_file.close()

if __name__ == "__main__":
    main()
