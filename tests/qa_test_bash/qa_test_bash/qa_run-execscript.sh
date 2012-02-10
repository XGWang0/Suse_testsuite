#!/bin/sh
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: run-execscript
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
#          USAGE: ./qa_run-execscript.sh 
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


echo run-execscript 
echo "warning: The text of a system error message may vary between systems and produce diff output." >&2
echo "warning: If the text of the error messages concerning \`notthere' or \`/tmp/bash-notthere' not being found or \`/' being a directory produce diff output, please do not consider this a test failure." >&2
echo "warning: if diff output differing only in the location of the bash binary appears, please do not consider this a test failure." >&2
cd /usr/share/qa/qa_test_bash/data/tests
sh run-execscript 2&> /tmp/run-execscript
 
                 

  if [ -s /tmp/run-execscript ]
  then    
    FAILED="1"
    echo "Diff is not empty!"
    echo "FAILED: bash test had an error :(" >&2
    cat /tmp/run-execscript
    rm /tmp/run-execscript
    exit 1
  else    
    echo "PASSED: bash run was ok :)"
    rm /tmp/run-execscript
    exit 0
  fi  
  
