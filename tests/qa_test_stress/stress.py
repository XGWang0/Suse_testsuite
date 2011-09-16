#!/usr/bin/python

import os


def count_cpus():
	"""number of CPUs in the local machine according to /proc/cpuinfo
	cpus = lines starting with 'processor' in /proc/cpuinfo"""
	f = file('/proc/cpuinfo', 'r')
	cpus = 0
	for line in f.readlines():
		if line.startswith('processor'):
			cpus += 1
	return cpus


if __name__ == "__main__":
	threads = 2*count_cpus()
	args = '-c %d -i %d -m %d -d %d -t 60 -v' % (threads, threads, threads, threads)
	os.system('/usr/bin/stress ' + args)


