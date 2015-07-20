#!/bin/bash

__import qavm/sq-control.sh
__import qavm/sq-global.sh
__import qavm/sq-util.sh

function sq_mach_open {
    if ! mkdir ${SQ_TEST_RUN_LOCK};then
        sq_error "There is already a qaset running"
        return 1
    fi
    __import conf/${SLE_RELEASE}.conf
    if test -f ${SQ_TEST_CONTROL_FILE_PREPARED};then
        sq_info "[MACH] Preparation: NOT NEED."
    else
        sq_info "[MACH] Preparation: is doing"
        sq_prep_repos_and_packages ${ARCH} ${SLE_BUILD} ${REPO_MIRROR}
        if test $? -ne 0;then
            sq_error "[MACH] preparation: failed!"
            return 1
        fi
        sq_info "[MACH] Preparation: disable snapper for btrfs"
        case ${SLE_BUILD} in
            SLE12*) snapper set-config TIMELINE_CREATE=no
        esac
        #reaim needs hostname entry in /etc/hosts
        sq_info "[MACH] Preparation: set hostname in /etc/hosts"
        echo "127.0.0.100    $(hostname)" >> /etc/hosts
        echo "$(date)" > ${SQ_TEST_CONTROL_FILE_PREPARED}
        sed -i /abuild/"s/^ *#*/#/" /etc/fstab
        if test $? -ne 0;then
            sq_info "[MACH] preparation:add comment in fstab failed!"
        fi

        # more kernel logs
        # TODO finally add to /etc/defautl/grub
        # kernel args : ignore_loglevel
        # xen kernel : multiboot args : loglvl=all guest_loglvl=all
        #              module line args : ignore_loglevel
        echo 8 >/proc/sys/kernel/printk
    fi
    SQ_TEST_MACH_FLAG_REBOOT=NO
}


function sq_mach_close {
    if test -d ${SQ_TEST_RUN_LOCK}; then
        rmdir ${SQ_TEST_RUN_LOCK}
    fi
    if test "X${SQ_TEST_MACH_FLAG_REBOOT}" == "XYES";then
        case ${SLE_RELEASE} in
            SLE11*) sq_os_reboot_2
                ;;
            *) sq_os_reboot
                ;;
        esac
    fi
}

function sq_mach_run {
    if sq_mach_open;then
        sq_control_run
    fi
    sq_mach_close
}
