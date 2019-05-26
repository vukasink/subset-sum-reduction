import matplotlib.pyplot as plot
import datetime
import time

def main():

	diagnostic_arr_1 = [[36, 5, 3.94004], [36, 31, 5.94905], [37, 8, 7.22474], [38, 24, 4.62027], [38, 27, 7.28248], [38, 29, 12.36864],
			[39, 12, 16.17715], [39, 13, 10.45035], [39, 14, 17.73045], [39, 15, 11.36457], [39, 22, 16.76803], [39, 28, 20.00003],
			[39, 30, 12.84638], [39, 32, 11.28872], [39, 37, 17.76786], [39, 39, 9.04546], [39, 44, 15.53773], [40, 7, 14.74811], [40, 10, 16.44521],
			[40, 17, 9.97996], [40, 20, 12.15335], [40, 23, 8.14417], [40, 40, 25.72396], [40, 46, 9.86822], [40, 48, 5.74918], [41, 2, 15.90464],
			[41, 36, 23.40664], [41, 38, 7.97929], [41, 41, 14.01125], [41, 43, 12.27942], [41, 49, 13.21893], [42, 3, 10.55466], [42, 4, 14.32041],
			[42, 16, 11.01234], [42, 26, 23.60859], [42, 34, 16.13048], [42, 35, 24.80072], [42, 42, 13.79838], [42, 50, 9.89217], [43, 9, 32.15582],
			[43, 19, 30.19531], [43, 47, 23.73424], [44, 6, 13.57943], [44, 21, 35.38401], [44, 25, 25.41914], [44, 33, 18.70123], [45, 1, 180.87444],
			[45, 45, 144.18693], [46, 11, 64.45141], [58, 18, 1100.19215]]
	diagnostic_arr_2 = [[36, 2, 4.94454], [37, 1, 7.22474], [38, 3, 8.09046], [39, 11, 14.45243], [40, 8, 12.85152], [41, 6, 14.46669],
			[42, 8, 15.51472], [43, 3, 28.69512], [44, 4, 23.27095], [45, 2, 162.53069], [46, 1, 64.45141], [47, 0, 0], [48, 0, 0], [49, 0, 0], [50, 0, 0],
			[51, 0, 0], [52, 0, 0], [53, 0, 0], [54, 0, 0], [55, 0, 0], [56, 0, 0], [57, 0, 0], [58, 1, 1100.19215]]
	
	min_block = min( [mem[0] for mem in diagnostic_arr_1] )
	min_time = min( [mem[2] for mem in diagnostic_arr_1] )
	max_block = max( [mem[0] for mem in diagnostic_arr_1] )
	max_time = max( [mem[2] for mem in diagnostic_arr_1] )

	plot.figure(figsize=(10.8,7.2), dpi=300)
	
	plot.tick_params(axis='x', which='minor', bottom=False)
	plot.tick_params(axis='y', which='minor', length=3)
	plot.tick_params(axis='y', which='major', length=4.5)
	plot.tick_params(axis='x', which='major', length=4.5)
	plot.minorticks_on()
	
	plot.plot([mem[0] for mem in diagnostic_arr_1], [mem[2] / 60 for mem in diagnostic_arr_1], 'b.', label='individual running times', markersize=3)
	plot.plot([mem[0] for mem in diagnostic_arr_2], [mem[2] / 60 for mem in diagnostic_arr_2], 'rx', markersize=8, label='average running time')
	
	plot.ylim(bottom = 1)
	plot.axis([min_block - 0.5, max_block + 0.5, 0, (max_time + 60) // 60])
	plot.xticks(range(min_block, max_block, 1))
	
	plot.legend()
	plot.savefig('example.png', bbox_inches='tight')
if __name__ == "__main__":
    main()
