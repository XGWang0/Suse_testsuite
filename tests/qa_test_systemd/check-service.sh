#!/bin/bash

function check_the_service {
    local service=$1
    local cur_status=$2

    case $cur_status in
        'active')
            systemctl restart $service
            active_line=$(systemctl status ${service} | egrep '^\s*Active:')
            active_words=($active_line)
            if test ${active_words[1]} != active;then
                systemctl status ${service} -l
                exit 1
            fi
            ;;
        'inactive')
            systemctl start $service
            active_line=$(systemctl status ${service} | egrep '^\s*Active:')
            active_words=($active_line)
            if test ${active_words[1]} != active;then
                systemctl status ${service} -l
                exit 1
            fi
            systemctl stop ${service}
            ;;
        'failed')
            systemctl status ${service} -l
            exit 1
            ;;
        *) echo "TODO status ${cur_status}"
    esac
}

