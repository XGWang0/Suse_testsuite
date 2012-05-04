#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-rhs-exp
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
#          USAGE: ./qa_run-rhs-exp.sh 
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


echo run-rhs-exp 
cd /usr/share/qa/qa_test_bash/data/tests
sh run-rhs-exp 2&> /tmp/run-rhs-exp
 
                 

  if [ -s /tmp/run-rhs-exp ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-rhs-exp
    rm /tmp/run-rhs-exp
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-rhs-exp
    exit 0
  fi  
  
