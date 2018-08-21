import sys
import heapq

buildings = [tuple(map(int, line.strip().split())) for line in sys.stdin]
edges = [0] + sorted(set([l for l,h,r in buildings] + [r for l,h,r in buildings]))

#reversed because removing the last element is more eficient than the head
remaining = buildings[::-1]

#this is a heap to keep track of the buildings that overlap over i as we iterate
current = []
previousHeight = 0
for i in edges[:-1]:
	#add to the current window all buildings whose left is less than the query index
	while remaining and remaining[-1][0] <= i:
		l,h,r = remaining.pop()
		#as we cannot specify a key, notice how we flip right and left to sort by right
		heapq.heappush(current, (r, h, l))
	#remove from the current window all buildings whose right is less than the query index
	while current and current[0][0] <= i:
		heapq.heappop(current)
	#maximum height within the current window
	h = max(current, default=(0,0,0), key=lambda x: x[1])[1]

	if h != previousHeight:
		print(i, h, end=' ')
		previousHeight = h

print(edges[-1], 0)
