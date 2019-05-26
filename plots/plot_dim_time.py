import matplotlib.pyplot as plt
import datetime
import time

def main():
	arr = [
			[37, 0.919637, 6.45136],
			[37, 0.930477, 7.69523],
			[37, 0.919556, 7.96973],
			[37, 0.930348, 5.49591],
			[38, 0.920112, 9.84922],
			[38, 0.941316, 2.74225],
			[39, 0.941331, 8.79931],
			[39, 0.930330, 8.66426],
			[39, 0.941843, 6.32252],
			[39, 0.930235, 10.52732],
			[39, 0.919671, 10.39141],
			[39, 0.919731, 8.99733],
			[39, 0.930242, 9.30354],
			[40, 0.919567, 20.00505],
			[40, 0.941191, 14.72668],
			[40, 0.941862, 7.01304],
			[40, 0.930263, 6.69005],
			[40, 0.930618, 15.03079],
			[41, 0.941218, 14.50125],
			[41, 0.919746, 17.65521],
			[41, 0.930236, 3.83843],
			[41, 0.919748, 41.10569],
			[41, 0.919577, 11.38451],
			[41, 0.919689, 13.95892],
			[41, 0.941250, 28.6812],
			[41, 0.939364, 16.26178],
			[42, 0.941384, 14.44643],
			[42, 0.930327, 19.41142],
			[42, 0.930285, 16.51375],
			[42, 0.919703, 9.48043],
			[42, 0.930687, 7.82983],
			[43, 0.941282, 36.13652],
			[43, 0.941601, 26.73835],
			[43, 0.941483, 21.9076],
			[43, 0.941723, 32.52722],
			[43, 0.930457, 31.03684],
			[43, 0.930362, 37.3888],
			[44, 0.930499, 28.53448],
			[44, 0.930338, 19.63291],
			[44, 0.941281, 44.22325],
			[44, 0.919624, 16.87123],
			[44, 0.919599, 34.71052],
			[45, 0.941200, 63.1056],
			[45, 0.941390, 43.89634],
			[47, 0.941505, 39.52069],
			[47, 0.930314, 44.34138],
			[47, 0.941371, 82.39564]
			]
#	min_block = min( [mem[0] for mem in diagnostic_arr_1] )
#	min_time = min( [mem[2] for mem in diagnostic_arr_1] )
#	max_block = max( [mem[0] for mem in diagnostic_arr_1] )
#	max_time = max( [mem[2] for mem in diagnostic_arr_1] )
	
	min_time = 10 * [0]
	max_time = 10 * [0]

	min_time[0] = min([ elem[2] for elem in arr if elem[0] in [37, 38, 39] ])
	max_time[0] = max([ elem[2] for elem in arr if elem[0] in [37, 38, 39]])

	if (min_time[0] < 5):
		min_y = 0
	else:
		min_y = min_time[0] - 5

	max_y = max_time[0] + 5
	min_x = 0.9075
	max_x = 0.9525

	fig, ax = plt.subplots(2, 3, figsize=(14.8, 10))
	ax1 = ax[0][0]
	ax2 = ax[0][1]
	ax3 = ax[0][2]
	ax4 = ax[1][0]
	ax5 = ax[1][1]
	ax6 = ax[1][2]
#	fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.8,8))
	fig.suptitle('Solving 80-dim Subset Sum Problems using BKZ reduction of 83-dim lattices with pruning')

	# The data
	x1 = [ elem[1] for elem in arr if elem[0] == 37 ]
	y1 = [ elem[2] for elem in arr if elem[0] == 37 ]
	ax1.set_ylim([min_y, max_y])
	ax1.set_xlim([min_x, max_x])
	ax1.title.set_text("BKZ block size " + str(37))
	ax1.set_ylabel('seconds')

	x2 = [ elem[1] for elem in arr if elem[0] == 38 ]
	y2 = [ elem[2] for elem in arr if elem[0] == 38 ]
	ax2.set_ylim([min_y, max_y])
	ax2.set_xlim([min_x, max_x])
	ax2.title.set_text("BKZ block size " + str(38))

	x3 = [ elem[1] for elem in arr if elem[0] == 39]
	y3 = [ elem[2] for elem in arr if elem[0] == 39 ]
	ax3.set_ylim([min_y, max_y])
	ax3.set_xlim([min_x, max_x])
	ax3.title.set_text("BKZ block size " + str(39))

	min_time[1] = min([ elem[2] for elem in arr if elem[0] in [40, 41, 42] ])
	max_time[1] = max([ elem[2] for elem in arr if elem[0] in [40, 41, 42]])

	if (min_time[1] < 5):
		min_y = 0
	else:
		min_y = min_time[1] - 5

	max_y = max_time[1] + 5


	x4 = [ elem[1] for elem in arr if elem[0] == 40 ]
	y4 = [ elem[2] for elem in arr if elem[0] == 40 ]
	ax4.set_ylim([min_y, max_y])
	ax4.set_xlim([min_x, max_x])
	ax4.set_ylabel('seconds')
	ax4.title.set_text("BKZ block size " + str(40))
	
	x5 = [ elem[1] for elem in arr if elem[0] == 41 ]
	y5 = [ elem[2] for elem in arr if elem[0] == 41 ]
	ax5.set_ylim([min_y, max_y])
	ax5.set_xlim([min_x, max_x])
	ax5.title.set_text("BKZ block size " + str(41))
	ax5.set_xlabel('problem dimension')

	x6 = [ elem[1] for elem in arr if elem[0] == 42 ]
	y6 = [ elem[2] for elem in arr if elem[0] == 42 ]
	ax6.set_ylim([min_y, max_y])
	ax6.set_xlim([min_x, max_x])
	ax6.title.set_text("BKZ block size " + str(42))

	# Create the sub-plots, assigning a different color for each line.
	# Also store the line objects created
	ax1.plot(x1, y1, 'bx')
	ax2.plot(x2, y2, 'rx')
	ax3.plot(x3, y3, 'gx')
	ax4.plot(x4, y4, 'b+')
	ax5.plot(x5, y5, 'r+')
	ax6.plot(x6, y6, 'g+')
	
	plt.subplots_adjust(right=0.85)

	plt.savefig('example.png', dpi=300)
	plt.show()

	# Create the legend
#	fig.legend([l1, l2, l3],     # The line objects
#    labels=line_labels,   # The labels for each line
#         loc="center right",   # Position of legend
#        borderaxespad=0.1,    # Small spacing around legend box
#       title="Legend Title"  # Title for the legend
#      )

	# Adjust the scaling factor to fit your legend text completely outside the plot
	# (smaller value results in more space being made for the legend)

if __name__ == "__main__":
    main()
