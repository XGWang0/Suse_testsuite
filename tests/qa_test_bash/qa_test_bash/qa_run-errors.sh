#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-errors
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
#          USAGE: ./qa_run-errors.sh 
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


echo run-errors 
cd /usr/share/qa/qa_test_bash/data/tests
sh run-errors 2&> /tmp/run-errors
 
                 

  if [ -s /tmp/run-errors ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-errors
    rm /tmp/run-errors
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-errors
    exit 0
  fi  
  
