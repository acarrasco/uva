import sys
from itertools import chain, groupby
from functools import partial
from copy import deepcopy

def add_diagonal(wod):
	n = len(wod[0]) + 1
	wd = [[1] * n for _ in range(n)]
	for i, row in enumerate(wod):
		for j, v in enumerate(row):
			wdj = j + int(j >= i)
			wd[i][wdj] = v
	return wd

def fmt(solution):
	for i in solution:
		print(i)
	print()

def diagonal(fx_sequences):
	return [row[i] for i, row in enumerate(fx_sequences)]

def profitable_fx_sequence(rates, fx_sequences):
	profitable_sequences = [fxs for fxs in diagonal(fx_sequences) if fx_sequence_value(rates, fxs) > 1.01]
	return min(profitable_sequences, key=len, default=None)

def flatten(table):
	return chain(*table)

def pairs(fx_sequence):
	return list(zip(fx_sequence[:-1], fx_sequence[1:]))
	
def ops_to_fx_sequence(pairs):
	return list(flatten([p[0:-1] for p in pairs])) + [pairs[-1][-1]]

def min_fx_sequence_length(fx_sequences):
	return len(min(flatten(fx_sequences), key=len))

def fx_sequence_value(rates, fx_sequence):
	value = 1
	for i, j in pairs(fx_sequence):
		value *= rates[i][j]
	return value

def optimize_fx_sequence(fx_sequence, fx_sequences):
	def expand():
		for i, j in pairs(fx_sequence):
			yield fx_sequences[i][j]
	return ops_to_fx_sequence(list(expand()))

def generate_fx_sequences_through(i, j, k, fx_sequences):
	ij_fx_sequence = fx_sequences[i][j]
	yield fx_sequences[i][j]
	for n in range(1, len(ij_fx_sequence)):
		through_k = ij_fx_sequence[:n] + [k] + ij_fx_sequence[n:]
		yield optimize_fx_sequence(through_k, fx_sequences)
		
def arbitrage(rates):
	n = len(rates)
	def shorter_than_n(fx_sequence):
		return len(fx_sequence) <= n
		
	fx_sequences = [[[i, j] for j in range(n)] for i in range(n)]
	value = partial(fx_sequence_value, rates)
	old_fx_sequences = None
	while (old_fx_sequences != fx_sequences and
	       not profitable_fx_sequence(rates, fx_sequences)):
		old_fx_sequences = deepcopy(fx_sequences)
		#print(old_fx_sequences)
		for i in range(n):
			for j in range(n):
				for k in range(n):
					candidates = list(filter(shorter_than_n, generate_fx_sequences_through(i, j, k, old_fx_sequences)))
					#print('i=%s j=%s k=%s candidates=%s' % (i, j, k, [(x, value(x)) for x in candidates]))
					best = max(candidates, key=lambda x:(value(x), -len(x)))
					#print('best=%s' % (best,))
					fx_sequences[i][j] = max(fx_sequences[i][j], best, key=lambda x:(value(x), -len(x)))
	v = profitable_fx_sequence(rates, fx_sequences)
	if v:
		return ' '.join(str(x+1) for x in v)
	else:
		return 'no arbitrage sequence exists'
	

lines = sys.stdin.readlines()
while lines:
	n = int(lines.pop(0))
	without_diagonal = [[float(x) for x in line.split()] for line in lines[:n]]
	lines[:n] = []
	rates = add_diagonal(without_diagonal)
	#print(rates)
	print(arbitrage(rates))
