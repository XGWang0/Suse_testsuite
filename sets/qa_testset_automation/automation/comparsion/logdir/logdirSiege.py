from dod.siege import DODSiege
from logdir import *

class logDirRecordSiege(logDirRecord):
    dod_class_dict = {'qa_siege_performance': DODSiege}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordSiege, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/qa_siege_performance" % self.path
        logs['qa_siege_performance'] = default_log
        self.logs = logs
                            
