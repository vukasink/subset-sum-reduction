#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BKZ Command Line Client
"""

import logging
import re
import time

from collections import OrderedDict

from fpylll import BKZ as BKZ_FPYLLL, GSO, IntegerMatrix
from fpylll.tools.quality import basis_quality

from g6k.algorithms.bkz import naive_bkz_tour, pump_n_jump_bkz_tour
from g6k.siever import Siever
from g6k.utils.cli import parse_args, run_all, pop_prefixed_params
from g6k.utils.stats import SieveTreeTracer, dummy_tracer
from g6k.utils.util import load_prebkz, load_matrix_file 

def bkz_kernel(arg0, params=None, seed=None):
	"""
	Run the BKZ algorithm with different parameters.

	:param d: the dimension of the lattices to BKZ reduce
	:param params: parameters for BKZ:

		- bkz/alg: choose the underlying BKZ from
		  {fpylll, naive, pump_n_jump}

		- bkz/blocksizes: given as low:high:inc perform BKZ reduction
		  with blocksizes in range(low, high, inc) (after some light)
		  prereduction

		- bkz/pre_blocksize: prereduce lattice with fpylll BKZ up
		  to this blocksize

		- bkz/tours: the number of tours to do for each blocksize

		- bkz/extra_dim4free: lift to indices extra_dim4free earlier in
		  the lattice than the currently sieved block

		- bkz/jump: the number of blocks to jump in a BKZ tour after
		  each pump

		- bkz/dim4free_fun: in blocksize x, try f(x) dimensions for free,
		  give as 'lambda x: f(x)', e.g. 'lambda x: 11.5 + 0.075*x'

		- pump/down_sieve: sieve after each insert in the pump-down
		  phase of the pump

		- challenge_seed: a seed to randomise the generated lattice

		- dummy_tracer: use a dummy tracer which capture less information

		- verbose: print tracer information throughout BKZ run

	"""
	# Pool.map only supports a single parameter
	if params is None and seed is None:
		d, params, seed = arg0
	else:
		d = arg0

	# params for underlying BKZ/workout/pump
	dim4free_fun = params.pop("bkz/dim4free_fun")
	extra_dim4free = params.pop("bkz/extra_dim4free")
	jump = params.pop("bkz/jump")
	pump_params = pop_prefixed_params("pump", params)
	workout_params = pop_prefixed_params("workout", params)

	# flow of the bkz experiment
	algbkz = params.pop("bkz/alg")
	blocksizes = params.pop("bkz/blocksizes")
	blocksizes = eval("range(%s)" % re.sub(":", ",", blocksizes))
	blocksizes = [ (elem, 1) for elem in blocksizes ]
	pre_blocksize = params.pop("bkz/pre_blocksize")
	tours = params.pop("bkz/tours")
	
	basic_blocksizes = params.pop("bkz/basic_blocksizes")
	if (not basic_blocksizes == None):
		basic_blocksizes = parse_blocksizes(basic_blocksizes)
		basic_blocksizes = [ (elem, 0) for elem in basic_blocksizes ]
		#print(basic_blocksizes)

	pruning_blocksizes = params.pop("bkz/pruning_blocksizes")
	if (not pruning_blocksizes == None):
		pruning_blocksizes = parse_blocksizes(pruning_blocksizes)
		pruning_blocksizes = [ (elem, 1) for elem in pruning_blocksizes ]
		#print(pruning_blocksizes)

	if ((not basic_blocksizes == None) or (not pruning_blocksizes == None)):
		blocksizes = ([] if basic_blocksizes == None else basic_blocksizes) + ([] if pruning_blocksizes == None else pruning_blocksizes)
	
	max_blocksize = max([ elem[0] for elem in blocksizes ])

	file_in = params.pop("file_in")

	# misc
	verbose = params.pop("verbose")
	dont_trace = params.pop("dummy_tracer", False)
	
	challenge_seed = params.pop("challenge_seed")

	if (file_in == None):
		A, bkz = load_prebkz(d, s=challenge_seed, blocksize=pre_blocksize)
	else:
		A, bkz = load_matrix_file(file_in)

	MM = GSO.Mat(A, float_type="double",
				 U=IntegerMatrix.identity(A.nrows, int_type=A.int_type),
				 UinvT=IntegerMatrix.identity(A.nrows, int_type=A.int_type))

	g6k = Siever(MM, params, seed=seed)
	if dont_trace:
		tracer = dummy_tracer
	else:
		tracer = SieveTreeTracer(g6k, root_label=("bkz", d), start_clocks=True)
	
	algbkz = "fpylll"

	if algbkz == "fpylll":
		M = bkz.M
	else:
		M = g6k.M

	T0 = time.time()
	for blocksize_pair in blocksizes:
		blocksize = blocksize_pair[0]
		pruning_active = blocksize_pair[1]
		
		for t in range(tours):
			with tracer.context("tour", t):
				if algbkz == "fpylll":
					if pruning_active == 0:
						par = BKZ_FPYLLL.Param(blocksize,
											strategies=None,
											max_loops=1)
					else:
						par = BKZ_FPYLLL.Param(blocksize,
										strategies=BKZ_FPYLLL.DEFAULT_STRATEGY,
										max_loops=1)
					# see __call__ method in g6k/g6k-env/lib/python2.7/site-packages/fpylll/algorithms/bkz.py	
					bkz(par)
					
					if(blocksize == max_blocksize):
#						print(bkz.M.G)
#						print("asdasd")
						print(bkz.A)
#						gso = GSO.Mat(bkz.A, flags=GSO.ROW_EXPO and GSO.INT_GRAM)
#						print("going to print out basis of the lattice of gso object")
#						print(gso.B)
#						print("going to pring gram matrix of gso object")
#						print(gso.G)

				elif algbkz == "pump_and_jump":
					pump_n_jump_bkz_tour(g6k, tracer, blocksize, jump=jump,
										 dim4free_fun=dim4free_fun,
										 extra_dim4free=extra_dim4free,
										 pump_params=pump_params)
				else:
					raise ValueError("bkz/alg=%s not recognized." % algbkz)

			if verbose:
				slope = basis_quality(M)["/"]
				fmt = "{'alg': '%25s', 'jump':%2d, 'pds':%d, 'extra_d4f': %2d, 'beta': %2d, 'slope': %.5f, 'total walltime': %.3f}" # noqa
				print fmt % (algbkz + "+" + ("enum" if algbkz == "fpylll" else g6k.params.default_sieve),
							 jump, pump_params["down_sieve"], extra_dim4free,
							 blocksize, slope, time.time() - T0)

	tracer.exit()
	try:
		return tracer.trace
	except AttributeError:
		return None


def bkz_tour():
	"""
	Run bkz tours.

	..	note :: that by default no information is printed.
		To enable set ``--dummy-tracer False`` and ``--verbose``.

	"""
	description = bkz_tour.__doc__

	args, all_params = parse_args(description,
								  bkz__alg="pump_and_jump",
								  bkz__blocksizes="40:51:2",
								  bkz__pre_blocksize=39,
								  bkz__tours=1,
								  bkz__extra_dim4free=0,
								  bkz__jump=1,
								  bkz__dim4free_fun="default_dim4free_fun",
								  pump__down_sieve=True,
								  challenge_seed=0,
								  dummy_tracer=True,  # set to control memory
								  verbose=False
								  )

	stats = run_all(bkz_kernel, all_params.values(),
					lower_bound=args.lower_bound,
					upper_bound=args.upper_bound,
					step_size=args.step_size,
					trials=args.trials,
					workers=args.workers,
					seed=args.seed)

	inverse_all_params = OrderedDict([(v, k) for (k, v) in all_params.iteritems()])

	stats2 = OrderedDict()
	for (n, params), v in stats.iteritems():
		params_name = inverse_all_params[params]
		params_name = re.sub("'challenge_seed': [0-9]+,", "", params_name)
		params = params.new(challenge_seed=None)
		stats2[(n, params_name)] = stats2.get((n, params_name), []) + v
	stats = stats2

	for (n, params) in stats:
		stat = stats[(n, params)]
		if stat[0]:  # may be None if dummy_tracer is used
			cputime = sum([float(node["cputime"]) for node in stat])/len(stat)
			walltime = sum([float(node["walltime"]) for node in stat])/len(stat)
			fmt = "%48s :: n: %2d, cputime :%7.4fs, walltime :%7.4fs"
			logging.info(fmt % (params, n, cputime, walltime))

def parse_blocksizes(blocksizes):
	if ":" in blocksizes:
		return eval("range(%s)" % re.sub(":", ",", blocksizes))
	# else suppose the format is x1.x2.x3... ->
	# that represents exactly the list of single betas
	else:
		return eval("[%s]" % re.sub("\.", ",", blocksizes))


if __name__ == '__main__':
	bkz_tour()
