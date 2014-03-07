HOW
===

simply run the set
------------------
    TARGET_RELEASE=SLE12
    RUN_LIST=SLE12
    ./sq-set.sh run -t ${TARGET_RELEASE} -s performance -l ${RUN_LIST}

call via a systemd service
--------------------------
  /usr/lib/systemd/system/sqperf.service when being packaged.
  NOTE some scripts are done in qa_testset_performance.spec.

skip the reboot
---------------
  set SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=YES in sq-control.sh to skip reboot

initialize the run list
-----------------------
    ./sq-set.sh reset
  which is just to delete the DONE file and empty NEXT_RUN file.

merely prepare repos and packages
---------------------------------
    ./sq-set.sh prepo

TODO
====
  * create /abuild
  * merge *.conf files
  * subcmd to stop run list.

