#!/usr/bin/python
import sys
import time

def collatz(p):
	t0=time.time()
	n=13**(3000*p)
	while n!=1:
		if n%2==0:
			n=n/2
		else:
			n=3*n+1
	t=(time.time()-t0)
	print str(p)+str('\t')+str(t)
print "collatz iteration"
print "depth\ttime"
for i in range(1,5,1):
	collatz(i)
