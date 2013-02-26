#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-intl
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
#          USAGE: ./qa_run-intl.sh 
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
export LC_ALL='en_US.UTF-8'

${THIS_SH} --version


rm -f /tmp/xx


echo run-intl 
echo "warning: some of these tests will fail if you do not have UTF-8 locales installed on your system." >&2
echo "warning: please ignore any differences consisting only of white space" >&2
cd /usr/share/qa/qa_test_bash/data/tests
sh run-intl 2&> /tmp/run-intl
 
                 

  if [ -s /tmp/run-intl ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-intl
    rm /tmp/run-intl
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-intl
    exit 0
  fi  
  
