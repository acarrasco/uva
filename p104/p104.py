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

def flatten(table):
	return chain(*table)

def pairs(fx_sequence):
	return list(zip(fx_sequence[:-1], fx_sequence[1:]))
	
def ops_to_fx_sequence(pairs):
	return list(flatten([p[0:-1] for p in pairs])) + [pairs[-1][-1]]

def fx_sequence_value(rates, fx_sequence):
	value = 1
	for i, j in pairs(fx_sequence):
		value *= rates[i][j]
	return value

def fmt(v):
	if v:
		return ' '.join(str(x+1) for x in v)
	else:
		return 'no arbitrage sequence exists'

def arbitrage(rates):
	n = len(rates)
	fx = [[{1: (rates[i][j], [i, j])} for j in range(n)] for i in range(n)]
	def value(x):
		return x[0]
	def concat(ij, k):
		ijv, ijs = ij
		kv, ks = k
		return (ijv * kv, ijs[:-1] + ks)
	for s in range(2, n+1):
		for i in range(n):
			for j in range(n):
				fx[i][j][s] = fx[i][j][s-1]
				for k in range(n):
					fx[i][j][s] = max(fx[i][j][s], concat(fx[i][k][s-1], fx[k][j][1]), key=value)
					if i == j and value(fx[i][j][s]) > 1.01:
						return fx[i][j][s][1]
	return None
	

lines = sys.stdin.readlines()
while lines:
	n = int(lines.pop(0))
	without_diagonal = [[float(x) for x in line.split()] for line in lines[:n]]
	lines[:n] = []
	rates = add_diagonal(without_diagonal)
	print(fmt(arbitrage(rates)))
