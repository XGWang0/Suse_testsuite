#!/bin/bash

function check_runlevel {
    local FAILSTATUS
    local rl
    local rl_words
    local ret
    FAILSTATUS=None
    #runlevel
    rl=$(runlevel)
    echo "runlevel: $rl"
    rl_words=($rl)
    if test "X${rl_words[0]}" != "XN";then
        FAILSTATUS=Y
    else
        case "${rl_words[1]}" in
            "0") : ;;
            "1") : ;;
            "2") : ;;
            "3") : ;;
            "4") : ;;
            "5") : ;;
            "6") : ;;
            "*") FAILSTATUS=Y
        esac
    fi
    if test "X${FAILSTATUS}" != XNone;then
        echo "check_runlevel FAILED"
        ret=1
    else
        echo "check_runlevel succeeded"
        ret=0
    fi
    return $ret
}

G_FAILSTATUS=None
check_runlevel || G_FAILSTATUS=Y

if test "X${G_FAILSTATUS}" != XNone;then
    ret=1
else
    ret=0
fi
exit $ret
