#! /bin/bash

# see bug #355611
# https://bugzilla.novell.com/show_bug.cgi?id=355611

function calldate
{
  date "$@" || exit 2
}

# This checks that $1 is a leap year.  It tests for the existence of
# $1-02-29, that $1-02-28 23:59 + 120 seconds is $1-02-29 00:01,
# that $1-02-28 23:59 + 1 day + 120 second is $1-03-01 00:01
function check_leap
{
  # sse == seconds since epoch
  sse_29=`calldate -d "$1-02-29 00:01" +%s`
  sse_28=`calldate -d "$1-02-28 23:59" +%s`
  # force format to be YY-MM-DD HH:MM
  date_28p=`calldate -d"@$(($sse_28 + 120))" +"%F %R"`
  date_28pp=`calldate -d"@$(($sse_28 + 120 + 24*3600))" +"%F %R"`
  sse_28p=`calldate -d "$date_28p" +%s`
  if test -z "$sse_29"; then
    echo "$1-02-29 doesn't exist"
    exit 1
  fi
  if test $sse_29 -ne $sse_28p; then
    echo "$1-02-29 00:01 doesn't match $1-02-28 23:59 + 120s ($sse_29 != $sse_28p)"
    exit 1
  fi
  if test "$date_28p" != "$1-02-29 00:01"; then
    echo "date for $1-02-28 23:59 + 120s is not '$1-02-29 00:01'"
    exit 1
  fi
  if test "$date_28pp" != "$1-03-01 00:01"; then
    echo "date for $1-02-28 23:59 + 1 day + 120s is not '$1-03-01 00:01'"
    exit 1
  fi
  return 0
}

# Similar to check_leap, only that it tests that the given year is _not_ a leap
# year
function check_non_leap
{
  if date -d "$1-02-29 00:01" > /dev/null 2>&1; then
    echo "date accepts $1-02-29, strange, but non-fatal"
  fi
  sse_28=`calldate -d "$1-02-28 23:59" +%s`
  # force format to be YY-MM-DD HH:MM
  date_28p=`calldate -d"@$(($sse_28 + 120))" +"%F %R"`
  sse_28p=`calldate -d "$date_28p" +%s`
  if test "$date_28p" != "$1-03-01 00:01"; then
    echo "date for $1-02-28 23:59 + 120s is not '$1-03-01 00:01'"
    exit 1
  fi
  return 0
}

LANG=C
year=1970
while test $year -lt 2038; do
  isleap=no
  if test $((year%4)) -eq 0; then
    if test $((year%100)) -ne 0; then
      isleap=yes
    elif test $((year%400)) -eq 0; then
      isleap=yes
    fi
  fi
  if test $isleap = yes; then
    check_leap $year
  else
    check_non_leap $year
  fi
  year=$(($year+1))
done
exit 0


