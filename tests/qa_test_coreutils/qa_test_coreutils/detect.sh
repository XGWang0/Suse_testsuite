#!/bin/sh
#detect the OS name by analysize /etc/issue 
#return s11/s11.1/s11.2 d11/d11.1/d11.2
#ostag=`cat /etc/issue|perl -ne 'if(/(\w+)\s+(\d+\.?\d+)\s+("?\w+)/i){$a=$1;$b=$2;$c=$3;$a=~s/^(.).*$/$1/;$c=~s/[[:alpha:]]//g;print $a,$b,".",$c}'`
ostag=`cat /etc/issue|perl -ne 'if(/(\w+)\s+(\d+\.?\d+)\s+("?\w+)/i){$b=$2;$c=$3;$c=~s/[[:alpha:]]|\"//g;$a=$b.".".$c;$a=~s/\.$//;print $a;}'`
