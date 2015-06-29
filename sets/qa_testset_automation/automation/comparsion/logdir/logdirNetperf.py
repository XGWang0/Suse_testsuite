from dod.netperf import DODNetperf
from logdir import *

class logDirRecordNetperf(logDirRecord):
    dod_class_dict = {'netperf-loop-tcp': DODNetperf,
                      'netperf-loop-udp': DODNetperf}
    def __getattr__(self, name):
        if name == 'logs':
            self._logs()
            return self.logs
        return super(logDirRecordNetperf, self).__getattr__(name)

    #todo parse more info

    def _logs(self):
        logs = dict()
        tcp_log = "%s/netperf-loop-tcp" % self.path
        logs['netperf-loop-tcp'] = tcp_log
        udp_log = "%s/netperf-loop-udp" % self.path
        logs['netperf-loop-udp'] = udp_log
        self.logs = logs
                            
