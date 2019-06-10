#!/bin/bash

min_N=10
max_N=10

for i in `seq $min_N $max_N`
do
	timestamp=$(date +"%d%m%Y_%X")
	logname="results/dim_84/fplll_set_04_$timestamp"
	script -c "python3 run_fplll_2.py $i" -a $logname
	sleep 3
done
