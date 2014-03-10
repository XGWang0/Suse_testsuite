#!/usr/bin/expect 
source /root/config
set timeout 6
set localip [lindex $argv 0]
puts $localip
#set apacheip 147.2.207.203
#set apacheip /sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:" 
spawn -noecho ssh $IP
#login 
expect {
        "not know" {send_user "[exec echo \"not know\"]";exit 2 }
        "(yes/no)?" { send "yes\r";exp_continue }
        #"password:" { send  "$pwd\r";exp_continue }
        #"No route to host" {send_user "[exec echo \"No route to host]\"]"; exit 3 }
        #"Permission denied, please try again." { send_user "[exec echo \"Error:Password is wrong\"]";exit 4 }
        "Last login:" { send_user "\n" }
}
send "curl -f http://$localip/apparmor.html\r"
sleep 1
#succeed 
expect { 
 #-re "test" {send_user "test pass" ; exit 0}
 #-re "curl" {send_user "test failed" ;exit 1}
 -re "test"  {exit 0}
 -re "error" {exit 1}
}
#expect timeout {exit 2}
exit
	


#expect "*#"
#send "exit\r"
