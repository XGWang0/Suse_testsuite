import dod
import logDB
import logging
import parserManager

perfdb = logDB.get_perfdb()

def log_perf_get_statistic(release, build, arch, host, suite, case):
    try:
        logurls = perfdb.get_logdir_by_run(release, build, arch,
                                           host, suite)
    except Exception as e:
        #TODO more fined control
        raise(e)
    urls = list()
    for ll in logurls:
        logfile = "/".join((ll, case))
        urls.append(logfile)
        logging.debug("[app] logfile url %s" % logfile)

    return parserManager.get_statistic_from_urls(suite, case, urls)


def log_perf_get_statistic_comparsion(arch, host, suite, case,
                                      release1, build1,
                                      release2, build2):
    rdod = dod.DictOfDict()
    dod1 = log_perf_get_statistic(release1, build1, arch, host, suite, case)
    dod2 = log_perf_get_statistic(release2, build2, arch, host, suite, case)
    rdod["%s/%s" % (release1, build1)] = dod1
    rdod["%s/%s" % (release2, build2)] = dod2

    if len(dod1) == 0 or len(dod2) == 0:
        rdod["comparsion"] = None
    else:
        rdod["comparsion"] = dod.DODOperator.comparsion(dod1, dod2)
    return rdod
