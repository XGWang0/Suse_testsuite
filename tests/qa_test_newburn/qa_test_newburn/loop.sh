#!/bin/sh
#prevent output of finished message on infinite loop test 

if [ $# -lt 3 ];then
echo 'syntax error on exec command'
exit
fi

while :
do
  $*
  echo $*
  exit
done
