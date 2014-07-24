#!/bin/bash

FAILED_STATUS=None
FAILED_UNIT_COUNT=0

function check_the_service {
    local service=$1
    local cur_status=$2

    case $cur_status in
        'active')
            systemctl restart $service
            active_line=$(systemctl status ${service} | egrep '^\s*Active:')
            active_words=($active_line)
            if test ${active_words[1]} != active;then
                FAILED_STATUS=Y
                FAILED_UNIT_COUNT=$(($FAILED_UNIT_COUNT + 1))
                systemctl status ${service}
            fi
            ;;
        'inactive')
            systemctl start $service
            active_line=$(systemctl status ${service} | egrep '^\s*Active:')
            active_words=($active_line)
            if test ${active_words[1]} != active;then
                #FAILED_STATUS=Y
                #FAILED_UNIT_COUNT=$(($FAILED_UNIT_COUNT + 1))
                systemctl status ${service}
            fi
            systemctl stop ${service}
            ;;
        'failed')
            systemctl status ${service}
            ;;
        *) echo "TODO status ${cur_status}"
    esac
}

while read line
do
    words=($line)
    service=${words[0]}
    status=${words[1]}
    if test "X${status}" == Xmasked;then
        continue
    fi
    echo $service | egrep '.*@.service$' > /dev/null
    if test $? -eq 0;then
        echo [DEBUG] $service is a pattern
        continue
    fi
    #ignore list
    case $service in
        # have someting with sound hardware
        alsa*) continue;;
        # poweroff is called in this service
        console-shell.service) continue;;
        # services about network
        network.service) continue;;
        sshd.service) continue;;
        wicked*) continue;;
        # services about installation
        YaST2*) continue;;
        # firewall related, they would block the ssh conection.
        SuSEfirewall*) continue;;
        # reboot power related
        systemd-reboot.service) continue;;
        systemd-remount-fs.service) continue;;
        systemd-shutdownd.service) continue;;
        systemd-suspend.service) continue;;
        systemd-hibernate.service) continue;;
        systemd-hybrid-sleep.service) continue;;
        systemd-halt.service) continue;;
        systemd-poweroff.service) continue;;
        systemd-kexec.service) continue;;
        rescue.service) continue;;
        # inird should not be run there
        dracut*) continue;;
        initrd*) continue;;
        # skip plymouth services
        plymouth*.service) continue;;
        # know oneshot service
        # more need to be done with oneshot services
        ntp-wait.service) continue;;
        kexec-load.service) continue;;
        kdump.service) continue;;
        klog.service) continue;;
        purge-kernels.service) continue;;
        sqperf.service) continue;; # qa_testset_performance
        # seems could not stop
        auditd.service) continue;;

    esac
    active_line=$(systemctl status ${service} | egrep '^\s*Active:')
    if test "X${active_line}" == X;then
        echo FAILED systemctl status ${service}
        continue
    fi
    active_words=($active_line)
    echo "[DEBUG] checking ${service}"
    check_the_service ${service} ${active_words[1]}
done < <(systemctl -l -t service --no-legend --no-pager list-unit-files)

if test "X${FAILED_STATUS}" != XNone;then
    if test ${FAILED_UNIT_COUNT} -eq 1;then
        echo "${FAILED_UNIT_COUNT} unit FAILED"
    else
        echo "${FAILED_UNIT_COUNT} units FAILED"
    fi
    ret=1
else
    echo "All units succeeded"
    ret=0
fi

exit $ret
