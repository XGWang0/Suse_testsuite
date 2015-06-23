
from common import dictOfList
from qadb import *
from dod.dodrender import DODRenderCLSimple
from dod import *
from logdir.logdirKernbench import *


logdir = LogDir('debug/logdir')
systemlog = LogDirComponent(logdir, 'system')


system_kernbench_sp3_GA_url_list = (
   'http://w3.suse.de/~rd-qa/Results/ProductTests/SLES-11/RC2/x86_64/apac2-ph027.apac.novell.com/kernbench-2015-05-23-14-41-16/',)
   #'http://w3.suse.de/~rd-qa/Results/ProductTests/SLES-11/RC2/x86_64/apac2-ph027.apac.novell.com/kernbench-2015-05-23-14-24-49/')

#not real data used to test
system_kernbench_sp4_RC1_url_list = (
    'http://w3.suse.de/~rd-qa/Results/ProductTests/SLES-11/RC2/ia64/ia64ph1007/tiobench-basic-2015-05-28-14-56-20/',
)

def get_dodgroup_from_url_list(url_list, record_cls, log_component, downloadp = True):
    group = QADBGroup(url_list)
    logdir_group = logDirRecordGroup(log_component, group, record_cls)
    if downloadp:
        group.download(logdir_group.path)
    logs = dictOfList()
    dod_class_dict = logdir_group.dod_class_dict
    for log_name in logdir_group.logs:
        logs[log_name] = list()
        for fpath in logdir_group.logs[log_name]:
            fd = open(fpath)
            logs[log_name].append(dod_class_dict[log_name](fd))
    dod_group_dict = dict()
    for log_name in logs:
        dod_group_dict[log_name] = DODGroup(logs[log_name], name = log_name)
    return dod_group_dict

system_kernbench_sp3_GA_dod_group = get_dodgroup_from_url_list(system_kernbench_sp3_GA_url_list,
                                                          logDirRecordKernbench, systemlog, downloadp = False)
for log_name in system_kernbench_sp3_GA_dod_group:
    dod_group = system_kernbench_sp3_GA_dod_group[log_name]
    dod_group_statistic = dod_group.statistic
    dod_group.append(dod_group_statistic)
    sp3_render = DODRenderCLSimple(dod_group, dod_group.name)
    sp3_render.render()



