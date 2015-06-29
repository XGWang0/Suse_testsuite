from dod.reaim import DODReaim
from logdir import *

class logDirRecordReaim(logDirRecord):
    dod_class_dict = {'reaim-alltests': DODReaim,
                      'reaim-compute': DODReaim,
                      'reaim-disk': DODReaim,
                      'reaim-new_dbase': DODReaim,
                      'reaim-new_fserver': DODReaim,
                      'reaim-shared': DODReaim}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordReaim, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        alltests_log = "%s/reaim-alltests" % self.path
        logs['reaim-alltests'] = alltests_log
        compute_log = "%s/reaim-compute" % self.path
        logs['reaim-compute'] = compute_log
        disk_log = "%s/reaim-disk" % self.path
        logs['reaim-disk'] = disk_log
        dbase_log = "%s/reaim-new_dbase" % self.path
        logs['reaim-new_dbase'] = dbase_log
        fserver_log = "%s/reaim-new_fserver" % self.path
        logs['reaim-new_fserver'] = fserver_log
        shared_log = "%s/reaim-shared" % self.path
        logs['reaim-shared'] = shared_log
        self.logs = logs
                            
