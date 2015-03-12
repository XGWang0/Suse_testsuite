HOW to run the set
==================
All the scripts in under /usr/share/qa/qaset
There are server simple run scripts which are in run/.
A calling of /usr/share/qa/qaset/run/*-run starts the run.
For performance the run scipts is run/performance-run.
And a service used to start the run after each rebooting
is installed automatically.

the service
-------------------
For systemd the service is qaset.service
For sysv the service is qaset

The stages of the running of the set
===================================
TODO

Files of directoris
===================
global ones
-----------
/var/log/qaset is where global data store, it is create at the first time the script called.
/var/log/qaset/control is where files used to control the running store.
/var/log/qaset/log is where to backup log data of case running if it needs.
/var/log/qaset/runs is where to store the screen log of each case running.
/var/log/qaset/calls is where to store the man screen log of each running.

custom ones
-----------
/root/qaset/config
/root/qaset/list is the cunstom list

the case run list
=================
TODO

Define a custom run list
------------------------
Essentially, it is to define a list varible of bash in /root/qaset/list before running.
Each element of it is the name of a case run.
The name of it is SQ_TEST_RUN_LIST.

An example of it is like

    SQ_TEST_RUN_LIST=(
        bonnie_btrfs
        bonnie_ext3
        bonnie_xfs
        iozone_btrfs
        iozone_ext3
        iozone_xfs
    )

It will call functions related to each case run to finish one case running.
There is details about how to define a new case run in performance.set.

Default, there will be a reboot after each case run.
reboot function can be disable or enable by writing special forms in the list.
All special forms start with '_'.

For example
    SQ_TEST_RUN_LIST=(
        bonnie_btrfs
        _reboot_off
        bonnie_ext3
        bonnie_xfs
        _reboot_on
        iozone_btrfs
        iozone_ext3
        iozone_xfs
    )

_reboot_off disable the reboot function at the time it appears.
It will not disable the possible reboot at the end of the last case running.
So after running the first bonnie_btrfs the system will reboot anyway.
_reboot_on enable the reboot function again.

Alternativly the system will not reboot after meet a _reboot_off,
and will reboot again after meet a _reboot_on.

QADB
====
After each case running the ctcs2 log will be submitted to QADB.
By defautl the comment is the name of the case run.

Customize the comment of the submittion of QADB
-----------------------------------------------
TODO 

Useful tips
===========
When you find some issue during the runing, you call stop it by
   TODO

then the running will stop after the curren case run finishes.

When the issue fixed you restart the running.
TODO
NOTE: Actually running can not be resumed. So please take case of the run list
for each running.

TODO
====
  * more fined run lists.
  * extract the global preparation.
  * backup /var/log/message
  * splite performance into different list
