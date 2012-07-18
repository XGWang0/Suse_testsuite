#!/usr/bin/python
import sys
import time
	
def primo(p):
	t0=time.time()
	if p==1:
		n=837401
	elif p==2:
		n=3085939
	else:
		n=8859679
	a=True
	for i in range(3, int(n**0.5)+1, 2):
		if not n%i:
			a=False
	t=(time.time()-t0)
	print str(p)+str('\t')+str(t)
print "primo iteration"
print "depth\ttime"
for i in range(1,5,1):
	primo(i)
