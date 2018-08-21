# naive attempt that runs out of time.
# this is not efficient when there are a lot of very big buildings
# since the complexity will be proportional to the total size of the
# buildings instead the size of the input (number of buildings)
import sys

buildings = [tuple(map(int, line.strip().split())) for line in sys.stdin]
rightmost = max(r for l,h,r in buildings)
heightMap = [0] * (rightmost +1)

for l, h, r in buildings:
	for i in range(l, r):
		heightMap[i] = max(heightMap[i], h)

print(heightMap)
previousHeight = 0
for i, h in enumerate(heightMap):
	if h != previousHeight:
		print(i,h, end=' ')
		previousHeight = h

print(rightmost, 0)
