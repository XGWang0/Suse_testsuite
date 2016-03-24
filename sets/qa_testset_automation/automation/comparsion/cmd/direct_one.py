import dod.dodrender
from dod import *
import sys
import getopt
import dod.siege
import dod.iozone
import dod.lmbench
import dod.dbench
#import dod.libmicro
import dod.tiobench
import dod.bonniepp
import dod.sysbencholtp
import dod.kernbench
import dod.reaim
import dod.netperf
import dod.pgbench
import openapi.app

product = ''
release = ''
arch = ''
testsuite = ''
logname = ''
hostname = ''

pl=['SLES-12-SP0','SLES-12-SP1','SLES-12','SLES-11-SP3','SLES-11-SP4','SLES-12.1-SP1']
rl=['beta1','beta2','beta3','beta4','RC1','RC2','RC3','GMC','GMC2','GM','GA','RC6','RC3A']
al=['x86_64','xen0-x86_64','i586','ia64','ppc']
tl=['qa_siege_performance','kernbench','lmbench','libmicro-bench','sysbench_oltp_ext3','sysbench_oltp_xfs','sysbench_oltp_btrfs','sysbench-sys','netperf-peer-loop','netperf-peer-loop6','netperf-peer-fiber','netperf-peer-fiber6','reaim_disk_ext3','reaim_disk_xfs','reaim_disk_btrfs','qa_tiobench_async_ext3','qa_tiobench_async_xfs','qa_tiobench_async_btrfs','bonnie++_async_ext3','bonnie++_async_xfs','bonnie++_async_btrfs','bonnie++_fsync_ext3','bonnie++_fsync_xfs','bonnie++_fsync_btrfs','qa_iozone_doublemem_ext3','qa_iozone_doublemem_xfs','qa_iozone_doublemem_btrfs','dbench4_async_ext3','dbench4_async_xfs','dbench4_async_btrfs','pgbench_small_ro_ext3','pgbench_small_ro_xfs','pgbench_small_ro_btrfs','pgbench_small_rw_ext3','pgbench_small_rw_xfs','pgbench_small_rw_btrfs']
ll=['qa_siege_performance','kernbench','lmbench','libmicro-bench','sysbench-oltp','sysbench-cpu','sysbench-fileio','sysbench-memory','sysbench-mutex','sbench-threads','netperf-loop-udp','netperf-loop-tcp','netperf-fiber-tcp','netperf-fiber-udp','netperf-fiber-udp6','netperf-fiber-tcp6','reaim-ioperf','tiobench-doublemem-async','bonnie++-async','bonnie++-fsync','iozone-doublemem-async','iozone-doublemem-fsync','dbench4-async','dbench4-fsync','pgbench-small-ro','pgbench-small-rw']
cl=['3.12.53-60.30-default','3.12.49-11-default']

def Usage():
    print ('usage:')
    print ('-h,--help: print help message.')
    print ('-p, choose products,like:[0:SLES-12-SP0,1:SLES-12-SP1,2:SLES-12,3:SLES-11-SP3,4:LES-11-SP4]')
    print ('-r, choose release version:[0:beta1,1:beta2,2:beta3,3:beta4,4:RC1,5:RC2,6:RC3,7:GMC1,8:GMC2,9:GM,10:GA]')
    print ('-a, architecture:[0:x86_64,1:xen0-x86_64,2:i586,3:ia64,4:ppc].like:0,1')
    print ('-c, comment info,default:kernel version')
    print ('')
    print ('-t, choose tcf name of testsuite:[0:qa_siege_performance,1:kernbench,2:lmbench,3:libmicro-bench,4:sysbench_oltp_ext3,5:sysbench_oltp_xfs,6:sysbench_oltp_btrfs,7:sysbench-sys,8:netperf-peer-loop,9:netperf-peer-loop6,10:netperf-peer-fiber,11:netperf-peer-fiber6,12:reaim_disk_ext3,13:reaim_disk_xfs,14:reaim_disk_btrfs,15:qa_tiobench_async_ext3,16:qa_tiobench_async_xfs,17:qa_tiobench_async_btrfs,18:bonnie++_async_ext3,19:bonnie++_async_xfs,20:bonnie++_async_btrfs,21:bonnie++_fsync_ext3,22:bonnie++_fsync_xfs,23:bonnie++_fsync_btrfs,24:qa_iozone_doublemem_ext3,25:qa_iozone_doublemem_xfs,26:qa_iozone_doublemem_btrfs,27:dbench4_async_ext3,28:dbench4_async_xfs,29:dbench4_async_btrfs,30:pgbench_small_ro_ext3,31:pgbench_small_ro_xfs,32:pgbench_small_ro_btrfs,33:pgbench_small_rw_ext3,34:pgbench_small_rw_xfs,35:pgbench_small_rw_btrfs]')
    print ('-l, choose log name:[0:qa_siege_performance,1:kernbench,2:lmbench,3:libmicro-bench,4:sysbench-oltp,5:sysbench-cpu,6:sysbench-fileio,7:sysbench-memory,8:sysbench-mutex,9:sysbench-threads,10:netperf-loop-udp,11:netperf-loop-tcp,12:netperf-fiber-tcp,13:netperf-fiber-udp,14:netperf-fiber-udp6,15:netperf-fiber-tcp6,16:reaim-ioperf,17:tiobench-doublemem-async,18:bonnie++-async,19:bonnie++-fsync,20:iozone-doublemem-async,21:iozone-doublemem-fsync,22:dbench4-async,23:dbench4-fsync,24:pgbench-small-ro,25:pgbench-small-rw] ')
    print ('-n, hostname,like:"apac2-ph027.apac.novell.com"')
    print ("for example:python3 direct_one.py -p '1,1' -r '0,0' -a '0,0' -t '0,0' -l '0,0' -n 'apac2-ph027.apac.novell.com'")

def getpara(argv):
    try:
        global product
        global release
        global arch
        global testsuite
        global logname
        global hostname
        global comment

        opts,args = getopt.getopt(sys.argv[1:],"n:p:r:a:t:l:n:c:")
        if len(opts)<5:
            print ("please give me the params:-p product,-r release,-a arch,-t testsuite,-l logname -f filesystem -c comment")
            Usage()
            sys.exit(1)
        for op,value in opts:
            if op == "-p":
                product = value
            elif op == '-r':
                release = value
            elif op == '-a':
                arch = value
            elif op == '-t':
                testsuite = value
            elif op == '-l':
                logname = value
            elif op == '-n':
                hostname = value
            elif op == '-c':
                comment = value
            elif op == '-h':
                Usage()
                sys.exit(1)
    except getopt.GetoptError:
        print('params are not defined well!')

def splitpara(p,ln):
    r1 = ''
    r2 = ''

    r1=ln[int(p.split(",")[0])]
    r2=ln[int(p.split(",")[1])]
    if r1 is None:
        r1 = r2
    elif r2 is None:
        r2 = r1
    else:
        pass
    return r1,r2

#dod1 = app.log_perf_get_statistic('SLES-12-SP0', 'GM', 'x86_64',
#                                         'apac2-ph027.apac.novell.com',
#                                         'qa_siege_performance',
#                                         'qa_siege_performance')


def main(argv):
    getpara(argv)
    product1,product2 = splitpara(product,pl)
    release1,release2 = splitpara(release,rl)
    arch1,arch2 = splitpara(arch,al)
    comment1,comment2 = splitpara(comment,cl)
    #testsuite1,testsuite2 = splitpara(testsuite,tl)
    #logname1,logname2 = splitpara(logname,ll)
    print (product1,release1,arch1,hostname,testsuite,logname,comment1)
    print (product2,release2,arch2,hostname,testsuite,logname,comment2)
    dod1 = openapi.app.log_perf_get_statistic(product1,release1,arch1,hostname,testsuite,logname,comment1)
    dod2 = openapi.app.log_perf_get_statistic(product2,release2,arch2,hostname,testsuite,logname,comment2)

    comp = dod.DODLogList()
    comp.append(dod1)
    comp.append(dod2)

    comparsion = comp.compare()

    text_render = dod.dodrender.DODRenderCLComparsion(dod_list = [dod1,dod2, ],
                                                  dod_comparsion_list = [comparsion, ])

    text_render.render()


if __name__=="__main__":
    main(sys.argv)
