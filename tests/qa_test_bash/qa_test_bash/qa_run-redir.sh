#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-redir
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
#          USAGE: ./qa_run-redir.sh 
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


echo run-redir 
cd /usr/share/qa/qa_test_bash/data/tests
sh run-redir 2&> /tmp/run-redir
 
                 

  if [ -s /tmp/run-redir ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    echo "warning: the text of a system error message may vary between systems and" >&2
echo "warning: produce diff output." >&2
echo "warning: if the text of an error message concerning \`redir1.*' not being" >&2
echo "warning: found or messages concerning bad file descriptors produce diff" >&2
echo "warning: output, please do not consider it a test failure" >&2
    less /tmp/run-redir
    rm /tmp/run-redir
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-redir
    exit 0
  fi  
  
