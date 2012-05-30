#NumBench 1.0
#Hecho por Gonzalo C. R.
#Bajo licencia MIT

import sys
import time

#def escribir_resultado(p, n):
#	r=open('NumBench_Resultado.txt', 'w')
#	r.write(str('Resultado del Benchmark con potencia ')+str(p)+str(':\n')+str(n)+str(':\n'))
#	r.close()

def auxiliar(n):
	x=4*(n**2)
	return x
	
def bench(pot, esc):
	def f(p):
		t0=time.time()
		a=0
		b=1
		i=500000*p
		while i>0:
			a, b = b, a+b
			i=i-1 
		t=(time.time()-t0)
		return t
		
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
		return t

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
		return t
		
	def collatz(p):
		t0=time.time()
		n=13**(3000*p)
		while n!=1:
			if n%2==0:
				n=n/2
			else:
				n=3*n+1
		t=(time.time()-t0)
		return t

	def oro(p):
		t0=time.time()
		i=500000*p
		o=1.0
		while i>0:
			o=(1+o)**0.5
			i=i-1
		t=(time.time()-t0)
		return t

	a=f(pot)
#	print"-"
	b=pi(pot)
#	print"-"
	c=primo(pot)
#	print"-"
	d=collatz(pot)
#	print"-"
	e=oro(pot)
#	print"-"
	nota=1000-5*(a+b+c+d+e)/2
	print str(pot)+str('\t')+str(nota)
#	if esc==True:
#		escribir_resultado(pot, nota)

if (len(sys.argv)>1):
	potencia=sys.argv[1]
#	print potencia
	if type(potencia)==int or potencia<4:
		print "Ingrese una potencia valida para el benchmark"
		exit()
	try:
		if sys.argv[2]=="-e":
			escribir=True
	except:
		escribir=False
	bench(int(potencia), escribir)
else:
	print "Ingrese una potencia para el benchmark"
	exit()
