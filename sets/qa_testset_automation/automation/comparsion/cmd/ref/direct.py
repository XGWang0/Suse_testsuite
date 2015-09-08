import app
import dod.tiobench
import dod
import dod.dodrender

iozone_dod1 = app.log_perf_get_statistic('SLES-12-SP0', 'GM', 'xen0-x86_64',
                                         'apac2-ph022.apac.novell.com',
                                         'qa_tiobench_async_btrfs',
                                         'tiobench-doublemem-async')

iozone_dod2 = app.log_perf_get_statistic('SLES-12-SP1', 'beta2', 'xen0-x86_64',
                                         'apac2-ph022.apac.novell.com',
                                         'qa_tiobench_async_btrfs',
                                         'tiobench-doublemem-async')

comp = dod.DODLogList()
comp.append(iozone_dod1)
comp.append(iozone_dod2)

comparsion = comp.compare()

text_render = dod.dodrender.DODRenderCLComparsion(dod_list = [iozone_dod1, iozone_dod2, ],
                                                  dod_comparsion_list = [comparsion, ])

text_render.render()


