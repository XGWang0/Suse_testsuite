#!/usr/bin/python

# This tool runs LTP tests for a given amount of time and writes all
# output of failed tests into a log directory.
#
# Author:  Gernot Payer <gpayer@suse.de>

import os,glob
import sys,time
import signal
import re

LTPDir = '/usr/lib/ltp'
LTPTestcases = {}
LogDir = '/tmp/ltplog'
LogFile = 'ltp-stress.log'
TimeToRun = 86400	# Default is 1 day = 86400s
RunTests = ['quickhit','dio','fs','fsx','ipc','math','mm','pty','sched','syscalls']
MaxRuntime = 300
WriteHTML = 0
CheckSyslog = 0
SyslogFile = None
SyslogOutput = ''

# yes, this is dirty, but I don't care :)
BlackList = [] #['proc01',]

# Current running test case
WaitForPID = -1

Usage = """Usage: %s [-htldfrTb] [--html] [--syslog]
   -h              help
   -t <time>       time to run (default: %d seconds)
   -l <ltpdir>     path to LTP (default: %s)
   -d <logdir>     path to directory for logging (default: %s)
   -f <logfile>    name of main logfile (default: %s)
   -r <testgroups> list of testgroups, e.g. math,syscalls,mm (default: all)
   -T <time>       maximum runtime for a child in seconds (default: 300)
   -b <list>       blacklist of testcases, e.g. proc01,crash02,fork12 (default: none)
   --html          write main log file as html, log file name will be index.html
   --syslog        checks /var/log/messages for errors possibly induced by LTP
""" % (sys.argv[0],TimeToRun,LTPDir,LogDir,LogFile)

def checkParams():
	global LTPDir,LogDir,LogFile,RunTests,MaxRuntime,WriteHTML,CheckSyslog
	if len(sys.argv) == 1:
		return
	import getopt
	try:
		allopts = getopt.getopt(sys.argv[1:],'ht:l:d:f:r:T:b:',('html','syslog'))
	except getopt.GetoptError,e:
		print "Warning:",e
		print Usage
		sys.exit(1)
	opts = allopts[0]
	for o in opts:
		ok,ov = o
		if ok == '-h':
			print Usage
			sys.exit(0)
		elif ok == '-t':
			setTimeToRun(ov)
		elif ok == '-l':
			LTPDir = ov
		elif ok == '-d':
			LogDir = ov
		elif ok == '-f':
			if WriteHTML:
				print "Warning: you specified --html, so log file name will be index.html"
				continue
			LogFile = ov
		elif ok == '-r':
			RunTests = ov.split(',')
		elif ok == '-T':
			MaxRuntime = int(ov)
		elif ok == '-b':
			BlackList = ov.split(',')
		elif ok == '--html':
			WriteHTML = 1
			LogFile = 'index.html'
		elif ok == '--syslog':
			CheckSyslog = 1

def setTimeToRun(ts):
	global TimeToRun
	l = len(ts)
	num = int(ts[:l-1])
	suffix = ts[l-1:]
	if not suffix in ['s','m','h','d']:
		print "Error: Only s,m,h,d allowed as time suffixes"
		sys.exit(1)
	if suffix == 's':
		TimeToRun = num
	elif suffix == 'm':
		TimeToRun = num * 60
	elif suffix == 'h':
		TimeToRun = num * 3600
	elif suffix == 'd':
		TimeToRun = num * 86400

def scanTestcases():
	global LTPDir,LTPTestcases,RunTests,BlackList
	import re
	if LTPDir[0] != '/':
		LTPDir = os.getcwd()+'/'+LTPDir
	for rt in RunTests:
		f = file(LTPDir+'/runtest/'+rt)
		lines = f.readlines()
		f.close()
		for l in lines:
			l = l.strip()
			if len(l) == 0:
				continue
			if l[0] == '#':
				continue
			m = re.search('[ \t]+',l)
			tc = l[:m.start()]
			if tc in BlackList:
				print "Info: %s is blacklisted, ignoring testcase" % tc
				continue
			tcb = l[m.end():]
			LTPTestcases[tc] = tcb
	#print "DEBUG: LTPTestcases:",LTPTestcases

def checkUID():
	if os.getuid() != 0:
		print 'Error: must run as root!'
		sys.exit(1)

def prepareEnv():
	global LogDir,LogFile,LTPDir,WriteHTML,CheckSyslog,SyslogFile
	# prepare logging stuff
	import socket
	os.system('mkdir -p '+LogDir)
	f = file(LogDir+'/'+LogFile,'w')
	if WriteHTML:
		f.write('<html>\n<title>LTP results</title>\n<body>\n<pre>\n')
	f.write(socket.gethostname()+'\n')
	f.write(time.ctime()+'\n\n')
	if WriteHTML:
		f.write('Syslog error messages go to file <a href="syslog">syslog</a>\n\n')
	else:
		f.write('Syslog error messages go to file syslog\n\n')
	f.write('Failed LTP tests:\n\n')
	f.write('Time    Testcase   RetCode    Outputfile\n')
	f.write('----------------------------------------\n\n')
	f.close()
	# prepare ENV for LTP tests
	os.putenv('LTPROOT',LTPDir)
	tmpdir = '/tmp/runalltests-'+str(os.getpid())
	os.mkdir(tmpdir)
	os.putenv('TMP',tmpdir)
	os.putenv('TMPBASE','/tmp')
	p = os.getenv('PATH')
	os.putenv('PATH',p+':.')
	if CheckSyslog:
		SyslogFile = file('/var/log/messages','r')
		SyslogFile.seek(0,2) # seek to end of file
		# touch logfile
		f = file(LogDir+'/syslog','w')
		f.write('Filtered errors from /var/log/messages\n'+'-'*38+'\n\n')
		f.close()

def cleanupEnv():
	global WriteHTML,LogDir,LogFile,CheckSyslog,SyslogFile
	if WriteHTML:
		f = file(LogDir+'/'+LogFile,'a')
		f.write('\n</pre>\n</body>\n</html>')
		f.close()
	os.system('rm -r $TMP')
	if CheckSyslog:
		SyslogFile.close()
		if len(SyslogOutput) == 0:
			f = file(LogDir+'/syslog','w')
			f.write('No errors encountered.')
			f.close()

def log(t,tc,rc,outf):
	global LogDir,LogFile,WriteHTML
	f = file(LogDir+'/'+LogFile,'a')
	s = outf.rfind('/')
	if WriteHTML:
		f.write('%s  %s  %s  <a href="%s">%s</a>\n' % (time.ctime(t), tc, rc, outf[s+1:], outf[s+1:]))
	else:
		f.write('%s  %s  %s  %s\n' % (time.ctime(t), tc, rc, outf[s+1:]))
	f.close()

def randList(src):
	import copy,random
	l = copy.copy(src)
	rl = []
	while len(l) > 0:
		i = random.randint(0,len(l)-1)
		rl.append(l[i])
		del(l[i])
	return rl

def runTests():
	global TimeToRun,LogDir,LTPTestcases,LTPDir,CheckSyslog
	endTime = time.time() + TimeToRun
	while time.time() < endTime:
		randtc = randList(LTPTestcases.keys())
		#print "DEBUG: randtc:",randtc
		for tc in randtc:
			print tc
			t = time.time()
			millis = '%.3f' % (t - int(t))
			timecode = time.strftime('%Y%m%dT%H%M%S', time.localtime(t)) + millis[1:]
			outf = LogDir + '/' + timecode + '-' + tc
			ret = spawnChild(tc,outf)
			if ret != 0:
				log(t, tc, ret, outf)
			if CheckSyslog:
				checkSyslog()
			if time.time() > endTime:
				return

def checkSyslog():
	global SyslogFile,LogDir,SyslogOutput
	syslogregexp = 'kernel.*(ECC:.(SBE|MBE)|NMI|3w-xxxx:.*Bad|stuck.*on.*IPI.*wait|warning|error|critical|lost.interrupt|scsi.:.aborting.command.due.to.timeout|VM:.*failed)'
	while 1:
		l = SyslogFile.readline()
		if len(l) == 0:
			return
		if re.search(syslogregexp, l) != None:
			f = file(LogDir+'/syslog','a')
			f.write(l)
			f.close()
			SyslogOutput += l

def alarmHandler(signum,frame):
	global WaitForPID
	if WaitForPID != -1:
		os.kill(WaitForPID, signal.SIGTERM)
		print "Info: child %s terminated (maximum runtime exceeded)" % WaitForPID

def sigHandler(signum,frame):
	if signum == signal.SIGQUIT:
		print "Warning: SIGQUIT (Quit from keyboard) recieved, ignored"

def spawnChild(tc,outf):
	global LTPDir,LTPTestcases,WaitForPID,MaxRuntime
	f = file(outf,'w')
	f.write(time.ctime()+'\n\n')
	pid = os.fork()
	if pid == 0: # child
		os.dup2(f.fileno(),sys.stdout.fileno())
		os.dup2(f.fileno(),sys.stderr.fileno())
		os.chdir(LTPDir+'/testcases/bin')
		os.execvp('sh',['/bin/sh', '-c', LTPTestcases[tc]] )
		print "Aieee! Beyond execvp!"
		sys.exit(1)
	else: # parent
		WaitForPID = pid
		signal.signal(signal.SIGQUIT,sigHandler)
		signal.signal(signal.SIGALRM,alarmHandler)
		signal.alarm(MaxRuntime)
		again = 1
		while again:
			try:
				cpid,status = os.waitpid(WaitForPID,0)
				again = 0
			except OSError: # Interrupted system call
				pass
			except KeyboardInterrupt:
				os.kill(WaitForPID,signal.SIGTERM)
				os.waitpid(WaitForPID,0)
				sys.exit(0)
		signal.alarm(0)
		WaitForPID = -1
		if cpid == -1:
			print "Error: an error occured during waitpid"
		if os.WIFEXITED(status):
			return os.WEXITSTATUS(status)
		if os.WIFSIGNALED(status):
			return os.WTERMSIG(status)
		return os.WSTOPSIG(status)
	
if __name__ == '__main__':
	checkParams()
	checkUID()
	scanTestcases()
	prepareEnv()
	print "Running for %s seconds..." % TimeToRun
	runTests()
	cleanupEnv()
	# print 'LTPDir: %s, LTPTestcases: %s, LogDir: %s, LogFile: %s, TimeToRun: %s' % (LTPDir, LTPTestcases, LogDir, LogFile, TimeToRun)
