#!/bin/bash

FAILED_STATUS=None
FAILED_UNIT_COUNT=0
while read line
do
    FAILED_STATUS=Y
    FAILED_UNIT_COUNT=$(($FAILED_UNIT_COUNT + 1))
    words=($line)
    systemctl -l status ${words[0]}
done < <(systemctl -l --failed --no-legend --no-pager)

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
