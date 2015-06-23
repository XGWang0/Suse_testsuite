from dod.bonniepp import DODBonniepp
from logdir import *

class logDirRecordBonniepp(logDirRecord):
    dod_class_dict = {'bonnie++-async': DODBonniepp}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordBonniepp, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/bonnie++-async" % self.path
        logs['bonnie++-async'] = default_log
        self.logs = logs
                            
