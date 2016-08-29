#	$OpenBSD: multiplex.sh,v 1.11 2005/04/25 09:54:09 dtucker Exp $
#	Placed in the Public Domain.

CTL=/tmp/openssh.regress.ctl-sock.$$

tid="connection multiplexing"

if grep "#define.*DISABLE_FD_PASSING" ${BUILDDIR}/config.h >/dev/null 2>&1
then
	echo "skipped (not supported on this platform)"
	exit 0
fi

DATA=/bin/ls${EXEEXT}
COPY=$OBJ/ls.copy
LOG=$TEST_SSH_LOGFILE

start_sshd

trace "start master, fork to background"
${SSH} -Nn2 -MS$CTL -F $OBJ/ssh_config -oSendEnv="_XXX_TEST" localhost &
MASTER_PID=$!

# Wait for master to start and authenticate
sleep 5

verbose "test $tid: envpass"
trace "env passing over multiplexed connection"
_XXX_TEST=blah ${SSH} -oSendEnv="_XXX_TEST" -S$CTL localhost sh << 'EOF'
	test X"$_XXX_TEST" = X"blah"
EOF
if [ $? -ne 0 ]; then
	fail "environment not found"
fi

verbose "test $tid: transfer"
rm -f ${COPY}
trace "ssh transfer over multiplexed connection and check result"
${SSH} -S$CTL localhost cat ${DATA} > ${COPY}
cmp ${DATA} ${COPY} || fail "1: ssh -Sctl: corrupted copy of ${DATA}"

rm -f ${COPY}
trace "ssh transfer over multiplexed connection and check result"
${SSH} -S $CTL localhost cat ${DATA} > ${COPY}
cmp ${DATA} ${COPY} || fail "2: ssh -S ctl: corrupted copy of ${DATA}"

rm -f ${COPY}
trace "sftp transfer over multiplexed connection and check result"
echo "get ${DATA} ${COPY}" | \
	${SFTP} -S ssh -oControlPath=$CTL localhost >$LOG 2>&1
cmp ${DATA} ${COPY} || fail "3: sftp: corrupted copy of ${DATA}"

rm -f ${COPY}
trace "scp transfer over multiplexed connection and check result"
${SCP} -S ssh -oControlPath=$CTL localhost:${DATA} ${COPY} >$LOG 2>&1
cmp ${DATA} ${COPY}|| fail "4: scp: corrupted copy of ${DATA}"

rm -f ${COPY}

for s in 0 1 4 5 44; do
	trace "exit status $s over multiplexed connection"
	verbose "test $tid: status $s"
	${SSH} -S $CTL localhost exit $s
	r=$?
	if [ $r -ne $s ]; then
		fail "exit code mismatch for protocol $p: $r != $s"
	fi

	# same with early close of stdout/err
	trace "exit status $s with early close over multiplexed connection"
	${SSH} -S $CTL -n localhost \
                exec sh -c \'"sleep 2; exec > /dev/null 2>&1; sleep 3; exit $s"\'
	r=$?
	if [ $r -ne $s ]; then
		fail "exit code (with sleep) mismatch for protocol $p: $r != $s"
	fi
done

trace "test check command"
${SSH} -S $CTL -Ocheck localhost || fail "check command failed" 

trace "test exit command"
${SSH} -S $CTL -Oexit localhost || fail "send exit command failed" 

# Wait for master to exit
sleep 2

kill -0 $MASTER_PID >/dev/null 2>&1 && fail "exit command failed" 
