HOW to run the set
==================
Because the set needs reboot so the calling is implemented as a service.
There are still methods to disable rebooting and enable it.

the systemd service
-------------------
The name of the service named sqperf.
Bt default sqperf is disable.
So you need to enable it by

    # systemctl enable sqperf

And then you can start it by

    # systemctl start sqperf

After that the set starts running.

The stages of the running of the set
===================================
Currently, the running of the whole set has two basic stage.
The first stage is preparation, and the second one is runing the list.

In the first stage what should be done includes adding repos, installing packages and
some initial works for the framework of the program. If there is some problem heppens,
you should mannual fix it, then resume the running.

In the second stage the factual running of cases happen there.
And the system could be rebooted in this stage.

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

the case run list
=================
Each release has its own default run list.
For example SLE12.list is the default run list for SLE12.
A custom run list can also be defined.

Define a custom run list
------------------------
Essentially, it is to define a list varible of bash in /root/qaset/config before running.
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
You can define variable SQ_TEST_QADB_COMMENT_TEMPLATE to customize the comment.
It is a template of the printf function in bash. Be default its value is just "%s"
Customize comment is designe with different cases run needs different comments in mind.
So in additon the varibale SQ_TEST_QADB_COMMENT_TEMPLATE, for each case run the function
sq_qadb_add_comment should be called in the _open functions.

TODO an example

Useful tips
===========
When you find some issue during the runing, you call stop it by

    # ./sq-set.sh stop

then the running will stop after the curren case run finishes.

When the issue fixed you restart the running.
    # ./sq-set.sh reset
    # reboot

NOTE: Actually running can not be resumed. So please take case of the run list
for each running.

TODO
====
  * more fined run lists.
  * extract the global preparation.
  * setup each preparation for each set.
  * backup /var/log/message
