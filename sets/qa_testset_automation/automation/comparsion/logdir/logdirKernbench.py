from dod.kernbench import DODKernbench
from logdir import *

class logDirRecordKernbench(logDirRecord):
    dod_class_dict = {'kernbench': DODKernbench}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordKernbench, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/kernbench" % self.path
        logs['kernbench'] = default_log
        self.logs = logs
                            
