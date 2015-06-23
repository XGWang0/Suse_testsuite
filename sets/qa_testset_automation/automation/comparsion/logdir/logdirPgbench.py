from dod.pgbench import DODPgbench
from logdir import *

class logDirRecordPgbench(logDirRecord):
    dod_class_dict = {'simple-pgbench-small-ro':DODPgbench,
                     'simple-pgbench-small-rw':DODPgbench}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordPgbench, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        ro_log = "%s/simple-pgbench-small-ro" % self.path
        logs['simple-pgbench-small-ro'] = ro_log
        rw_log = "%s/simple-pgbench-small-rw" % self.path
        logs['simple-pgbench-small-rw'] = rw_log
        self.logs = logs

