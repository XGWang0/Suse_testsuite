#!/bin/bash

phpini="/etc/php7/apache2/php.ini"
sysconfig="/etc/sysconfig/apache2"
#phpini="/tmp/php.ini"
#sysconfig="/tmp/apache2"

enforce_setting () {
   local attribute=$1
   local value=$2

   if [ -z "$attribute" ]; then return 1; fi

   grep -q -E "^[[:space:]]*$attribute[[:space:]]*=" $phpini
   if [ $? -gt 0 ]; then
      echo -e "\n;added by $0 on `date`\n$attribute = $value\n" >> $phpini
   else
      sed -i -r "s/^\s*$attribute\s*=.*/$attribute = $value/" $phpini
   fi
}

add_module () {
    local newmodule=$1

    grep -q -E "^[[:space:]]*APACHE_MODULES[[:space:]]*=" $sysconfig
    if [ $? -gt 0 ]; then
       echo "could not find APACHE_MODULES in $sysconfig ... please properly install apache2 first"
    else
       grep -q -E "^[[:space:]]*APACHE_MODULES[[:space:]]*=.*\W+$newmodule\W+" $sysconfig
       if [ $? -gt 0 ]; then
	  sed -i -r "s/^\s*APACHE_MODULES\s*=\s*\"/APACHE_MODULES=\"$newmodule /" $sysconfig
       else
	   echo "module $newmodule already present in $sysconfig"
       fi
    fi
}

cp -a $phpini $phpini.backup

enforce_setting html_errors Off
enforce_setting track_errors On
enforce_setting safe_mode Off
enforce_setting display_errors On
enforce_setting open_basedir ""
enforce_setting error_reporting "E_ALL|E_STRICT"

echo "the following changes have been made to $phpini:"
diff $phpini.backup $phpini

cp -a $sysconfig $sysconfig.backup

add_module php7

echo "the following changes have been made to $sysconfig:"
diff $sysconfig.backup $sysconfig

