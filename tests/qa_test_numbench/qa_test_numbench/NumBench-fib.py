#!/usr/bin/python
import sys
import time
def fib(p):
	t0=time.time()
	a=0
	b=1
	i=500000*p
	while i>0:
		a, b = b, a+b
		i=i-1 
	t=(time.time()-t0)
	print str(p)+str('\t')+str(t)
print "fibonacci iteration"
print "depth"+str('\t')+"time"
for i in range(1,5,1):
	fib(i)
