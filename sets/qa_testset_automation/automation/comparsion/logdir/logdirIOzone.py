from dod.iozone import DODIOZone
from logdir import *

class logDirRecordIOzone(logDirRecord):
    dod_class_dict = {'iozone-bigmem-default': DODIOZone,
                      'iozone-bigmem-fsync': DODIOZone}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordIOzone, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        default_log = "%s/iozone-bigmem-default" % self.path
        logs['iozone-bigmem-default'] = default_log
        sync_log = "%s/iozone-bigmem-fsync" % self.path
        logs['iozone-bigmem-fsync'] = sync_log
        self.logs = logs
