#!/bin/bash

source libqainternal.lib.sh

function test01() {
    RESULT=$FAILED
    
    if checkService "postfix"; then
        if restartService "postfix" && checkService "postfix"; then
            printMessage $MSG_PASSED "Postfix - restart the service"
            RESULT=$PASSED
        fi
    else
        printMessage $MSG_ERROR "Postfix is not running."
    fi

    if [ "$RESULT" = "$FAILED" ]; then
        printMessage $MSG_FAILED "Postfix - restart the service"
    fi
    return $RESULT
}


test01
exit $?
