#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-quote
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
#          USAGE: ./qa_run-quote.sh 
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


echo run-quote 
cd /usr/share/qa/qa_test_bash/data/tests
sh run-quote 2&> /tmp/run-quote
 
                 

  if [ -s /tmp/run-quote ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-quote
    rm /tmp/run-quote
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-quote
    exit 0
  fi  
  
