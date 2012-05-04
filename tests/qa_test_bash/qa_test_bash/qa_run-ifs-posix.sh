#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-ifs-posix
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
#          USAGE: ./qa_run-ifs-posix.sh 
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


echo run-ifs-posix 
cd /usr/share/qa/qa_test_bash/data/tests
sh run-ifs-posix 2&> /tmp/run-ifs-posix
 
                 

  if [ -s /tmp/run-ifs-posix ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-ifs-posix
    rm /tmp/run-ifs-posix
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-ifs-posix
    exit 0
  fi  
  
