#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-new-exp
#        VERSION: 0.1
#         AUTHOR: Klara Cihlarova <cihlarov@suse.cz>
#       REVIEWER: 
#        LICENSE: GPL
#
#        CREATED: 2008-1-17
#        REVISED: 2008-1-17
#
#    DESCRIPTION: "bash functionality test"
#   REQUIREMENTS: "bash"
#          USAGE: ./qa_run-new-exp.sh 
#
#===============================================================================                


FAILED="0"

PATH=/usr/share/qa/qa_test_bash/data:$PATH    # just to get recho/zecho/printenv if not run via `make tests'
export PATH

# unset BASH_ENV only if it is set
[ "${BASH_ENV+set}" = "set" ] && unset BASH_ENV
# ditto for SHELLOPTS
#[ "${SHELLOPTS+set}" = "set" ] && unset SHELLOPTS

: ${THIS_SH:=/bin/bash}
export THIS_SH

${THIS_SH} --version


rm -f /tmp/xx


echo run-new-exp 
echo "warning: two of these tests will fail if your OS does not support named pipes or the /dev/fd filesystem.  If the tests of the process substitution mechanism fail, please do not consider this a test failure." >&2
echo "warning: If you have exported variables beginning with the string _Q, diff output may be generated. If so, please do not consider this a test failure." >&2
cd /usr/share/qa/qa_test_bash/data/tests
sh run-new-exp 2&> /tmp/run-new-exp
 
                 

  if [ -s /tmp/run-new-exp ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    less /tmp/run-new-exp
    rm /tmp/run-new-exp
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-new-exp
    exit 0
  fi  
  
