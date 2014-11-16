#!/bin/sh
#
# File :         apacheremote.sh
#
# Description:   Test Apache server.
#                Test #1: visit local machine by command curl, expected success
#
# Author:        Jia Li , jli@suse.com
#
# History:       Jan 21 2014 - Created - Jia Li.
#
# Function:      Apache server
#
# Description:  - Check if can visit local machine by command curl.
#
# Input:        - $1 - calling test case.
#               - $2 - command that needs to be checked.
#
# Return:       - zero on success.
#               - non-zero on failure.
#<Declarations>
#</Declarations>

visitbrowser()
{
  export RC=0
  #curl -o $TMPROOT/page.html http://www.linuxidc.com|| FAILED="1"
  curl -f http://127.0.0.1/apparmor.html || RC=$?

  #OVERALL-RESULT
  if [ $RC -eq 0 ]
  then 
      echo "PASSED: visit pache server passed"
      return $RC
  elif [ $RC -eq 22 ]
  then
      echo "FAILED: The requested URL returned error" >&2
      return $RC
  else
      echo "FAILED: Unknown error,please check logs"
      return $RC
  fi
  return $RC
}


#main 
echo "test" > /srv/www/htdocs/apparmor.html ||exit $?

visitbrowser || exit $RC

rm -rf /srv/www/htdocs/apparmor.html ||exit $?

