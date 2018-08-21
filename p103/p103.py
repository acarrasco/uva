import sys

def nests(a, b):
	return all(i > j for i, j in zip(a, b)) * 1
	
def fmt(solution):
	print(len(solution))
	print(' '.join(str(x+1) for x in solution))

def solve(boxes):
	n = range(len(boxes))
	#to speed up comparisons
	for box in boxes: box.sort
	#matrix representation of the nesting relation
	f = [[nests(a, b) for b in boxes] for a in boxes]
	#solutions vector, w[i] holds the longest nesting sequence starting from i (so far)
	w = [[]] * len(boxes)
	for i in n:
		#the boxes that can't nest any other have a longest nesting sequence made up of just themselves
		if not any(f[i]):
			w[i] = [i]
	old_w = None
	#when the solution vector doesn't change we are done
	while old_w != w:
		old_w = w[::]
		for i in n:
			for j in n:
				#if the box i can nest the box j and a longest sequence starting from j has already been computed
				if f[i][j] and w[j]:
					#if starting from j yields a longer sequence, update the best solution so far
					w[i] = max(w[i], w[j]+[i], key=len)
	return max(w, key=len)

lines = [list(map(int, x.strip().split())) for x in sys.stdin]
while lines:
	nboxes, dimensions = lines.pop(0)
	solution = solve(lines[:nboxes])
	fmt(solution)
	lines[:nboxes] = []
