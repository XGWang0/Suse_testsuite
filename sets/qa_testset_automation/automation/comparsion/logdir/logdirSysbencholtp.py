from dod.sysbencholtp import DODSysbencholtp
from logdir import *

class logDirRecordSysbencholtp(logDirRecord):
    dod_class_dict = {'sysbench-oltp': DODSysbencholtp}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordSysbencholtp, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/sysbench-oltp" % self.path
        logs['sysbench-oltp'] = default_log
        self.logs = logs
                            
