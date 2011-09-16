#!/bin/bash

source libqainternal.lib.sh

function test01() {
    if checkService "postfix"; then
        if stopService "postfix"; then
            printMessage $MSG_PASSED "Postfix - stop the service"
            return $PASSED
        else
            printMessage $MSG_FAILED "Postfix - stop the service"
            return $FAILED
        fi
    else
        printMessage $MSG_FAILED "Postfix - stop the service: Postfix is not running."
        return $FAILED
    fi
}

test01
exit $?
