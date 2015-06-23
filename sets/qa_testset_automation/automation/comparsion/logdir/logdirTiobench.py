from dod.tiobench import DODTiobench
from logdir import *

class logDirRecordTiobench(logDirRecord):
    dod_class_dict = {'tiobench-basic': DODTiobench}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordTiobench, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/tiobench-basic" % self.path
        logs['tiobench-basic'] = default_log
        self.logs = logs
                            
