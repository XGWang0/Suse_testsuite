#!/bin/sh
echo "abc" > /srv/www/htdocs/apparmor.html || exit $?

eth=`ip route | grep default | awk '{print $5}'`
if [ -n $eth ]
then 
   localip=`/sbin/ifconfig $eth  | sed -n '/inet addr:/ s/inet addr://pg' | awk -F" " '{print $1}'`
#localip=`traceroute -m 1 google.com | grep '^ 1' | awk '{print $2}'`
else
   echo "Can't find eth"
fi 

if [ -n $localip ]    
then
    #x=`expect -f expect.ex $localip|tail -1`
    expect -f expect.ex $localip
    if [ $? -eq 0 ]
    then 
        echo "test passed!"
    elif [ $? -eq 1 ]
    then 
        echo "test failed!"
    else
        echo "Can't match any word,time out,test failed!"
    fi
fi
rm -rf /srv/www/htdocs/apparmor.html || exit $?

