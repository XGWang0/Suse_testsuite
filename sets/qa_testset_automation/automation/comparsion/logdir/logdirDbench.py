from dod.dbench import DODDbench
from logdir import *

class logDirRecordDbench(logDirRecord):
    dod_class_dict = {'dbench-default': DODDbench}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordDbench, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/dbench-default" % self.path
        logs['dbench-default'] = default_log
        self.logs = logs
                            
