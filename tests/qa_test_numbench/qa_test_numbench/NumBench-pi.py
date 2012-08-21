#!/usr/bin/python
import sys
import time

def auxiliar(n):
	x=4*(n**2)
	return x
def pi(p):
	t0=time.time()
	pi=1.0
	n=1.0
	i=500000*p
	while i>0:
		pi=(auxiliar(n)/(auxiliar(n)-1))*pi
		pin=pi*2
		n=n+1
		i=i-1
	t=(time.time()-t0)
	print str(p)+str('\t')+str(t)
print "pi iteration"
print "depth\ttime"
for i in range(1,5,1):
	pi(i)
