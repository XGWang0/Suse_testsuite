#!/usr/bin/python
import sys
import time

def oro(p):
	t0=time.time()
	i=500000*p
	o=1.0
	while i>0:
		o=(1+o)**0.5
		i=i-1
	t=(time.time()-t0)
	print str(p)+str('\t')+str(t)
print "oro iteration"
print "depth\ttime"
for i in range(1,5,1):
	oro(i)
