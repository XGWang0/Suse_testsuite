#!/bin/sh
for i in testing/tests/T*; do
    name=`basename $i`
    UPNAME=`echo $name | tr a-z A-Z`
    echo "timer 600"
    echo "fg 1 $UPNAME /usr/share/qa/qa_test_net-snmp/run-test-wrapper.sh $name"
    echo "wait"
    echo 
done

