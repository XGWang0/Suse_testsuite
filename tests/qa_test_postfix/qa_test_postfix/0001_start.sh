#!/bin/bash

source libqainternal.lib.sh


function test01() {
    if startService "postfix"; then
        printMessage $MSG_PASSED "Postfix - start the service"
        return $PASSED
    else
        printMessage $MSG_FAILED "Postfix - start the service"
        return $FAILED
    fi
}

test01
exit $?
