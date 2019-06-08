#!/bin/bash

min_N=9
max_N=9

for i in `seq $min_N $max_N`
do
	timestamp=$(date +"%d%m%Y_%r")
	logname="results/fplll_set_03_$timestamp"
#	cmd_name="\"python3 run_fplll_exclude_one_problem.py $i\""
#	echo $cmd_name
	script -c "python3 run_fplll_exclude_one_problem.py $i" -a $logname
done
