#	$OpenBSD: try-ciphers.sh,v 1.10 2005/05/24 04:10:54 djm Exp $
#	Placed in the Public Domain.

tid="try ciphers"

# Asking sshd binary for supported ciphers and macs
ciphers=$(sudo /usr/sbin/sshd -T | sed -n 's/^ciphers[[:blank:]]*\(.*\)/\1/p' | sed 's/,/ /g')
macs=$(sudo /usr/sbin/sshd -T | sed -n 's/^macs[[:blank:]]*\(.*\)/\1/p' | sed 's/,/ /g')

echo "Provided ciphers by sshd binary: $ciphers"
echo "Provided macs by sshd binary: $macs"

# List of basic ciphers and macs provided by Marcus Meissner in bsc#1001917
# The list should be compatible with SLE11 (but not GCM ciphers) and SLE12
ciphers_list="aes128-ctr aes192-ctr aes256-ctr aes128-gcm@openssh.com aes256-gcm@openssh.com" 
macs_list="hmac-sha1 hmac-sha2-256 hmac-sha2-512 hmac-sha1-etm@openssh.com hmac-sha2-256-etm@openssh.com hmac-sha2-512-etm@openssh.com"

for c in $ciphers_list; do
  echo $ciphers | grep -q $c
  if [ $? -ne 0 ]; then
    fail "FAILURE: Cipher $c not supported by sshd binary"
  fi
done

for m in $macs_list; do
  echo $macs | grep -q $m
  if [ $? -ne 0 ]; then
    fail "FAILURE: Mac $m not supported by sshd binary"
  fi
done

for c in $ciphers; do
	for m in $macs; do
		trace "proto 2 cipher $c mac $m"
		verbose "test $tid: proto 2 cipher $c mac $m"
		${SSH} -F $OBJ/ssh_proxy -2 -m $m -c $c somehost true
		if [ $? -ne 0 ]; then
			fail "ssh -2 failed with mac $m cipher $c"
		fi
	done
done

ciphers="3des blowfish"
for c in $ciphers; do
	trace "proto 1 cipher $c"
	verbose "test $tid: proto 1 cipher $c"
	${SSH} -F $OBJ/ssh_proxy -1 -c $c somehost true
	if [ $? -ne 0 ]; then
		fail "ssh -1 failed with cipher $c"
	fi
done

if ${SSH} -oCiphers=acss@openssh.org 2>&1 | grep "Bad SSH2 cipher" >/dev/null
then
	:
else

echo "Ciphers acss@openssh.org" >> $OBJ/sshd_proxy
c=acss@openssh.org
for m in $macs; do
	trace "proto 2 $c mac $m"
	verbose "test $tid: proto 2 cipher $c mac $m"
	${SSH} -F $OBJ/ssh_proxy -2 -m $m -c $c somehost true
	if [ $? -ne 0 ]; then
		fail "ssh -2 failed with mac $m cipher $c"
	fi
done

fi
