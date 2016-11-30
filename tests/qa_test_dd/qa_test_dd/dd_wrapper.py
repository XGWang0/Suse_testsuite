#!/usr/bin/python3
import re
import os
import signal
import sys
import time

class DdSuperViser:
  def __init__(self,config):
    self.config_file = config
    self.ddtest={}
    self.ddtest['inteval'] = 1 #report the statistics every 1 sec
    self.ddtest['timeout'] = 30 #timeout for the dd test
    self.sig = signal.SIGUSR1  # "SIGUSR1" 
  def load_config(self):
    self.path = os.path.dirname(os.path.abspath(__file__))
    re_key = {'inteval':r'^[^#]*moniter_inteval\s*=\s*(\d+)', 'timeout':r'^[^#]*timeout\s*=\s*(\d+)', 'cmd':r'^[^#]*(dd[^\n]+)'}
    try:
      with open(os.path.join(self.path,self.config_file)) as config_fd:
        for line in config_fd:
          for key in re_key.keys():
            match_result=re.search(re_key[key],line)
            if(match_result):
              self.ddtest[key]=match_result.group(1)

    except:
      print('open/parser test failed')
      raise
      sys.exit(1)
    self.ddtest['timeout'] = int(self.ddtest['timeout'])
    self.ddtest['inteval'] = int(self.ddtest['inteval'])

  def run(self):
    print(self.ddtest)
    try:
      self.pid = os.fork()
    except:
      print('for error')
      sys.exit(1)
    if(self.pid == 0):
      #we are child
      os.execv('/usr/bin/dd',self.ddtest['cmd'].split())
    else:
      time_run=0
      run_count=self.ddtest['timeout']/self.ddtest['inteval']
      #let the child start the dd
      time.sleep(self.ddtest['inteval'])

      while(time_run < run_count):
        ret_pid,ret_exit = os.waitpid(self.pid,os.WNOHANG)
        #print("the return pid is %s and exit code is %s time_run is %s run_count is %s slefpid is %s" % (ret_pid,ret_exit,time_run,run_count,self.pid))
        if (ret_pid == self.pid):
          break
        try:
          os.kill(self.pid,signal.SIGUSR1)
        except ProcessLookupError:
          pass
        time_run += 1
        time.sleep(self.ddtest['inteval'])
      (time_run == run_count) and os.kill(self.pid,signal.SIGKILL)
     

dd_run = DdSuperViser(sys.argv[1])
dd_run.load_config()
dd_run.run()


