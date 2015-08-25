#!/bin/bash

# {{{ overridable config
LOGF=/dev/null
TMP_BASEDIR=
# }}}

# {{{ hardcoded config
SVN_TEST_VERSION="0.1.1"
SVN_GRP="svn"
SVN_USR="svn"
SVN_HOME="/srv/svn"

SVN_CLI_USR="svntest"
SVN_CLI_HOME="/home/svntest"

SVN_APACHE_CONF=/etc/apache2/conf.d/subversion.conf
SVN_APACHE_CONF_BAK="${SVN_APACHE_CONF}.bak"

RES_OK=0
# RES_OK is not safe to redefine, the rest should work as long
# as they are not 0
RES_FAIL=1
RES_FAIL_INT=11
RES_FAIL_SETUP=11
RES_SKIPPED=22
# }}}

APACHE_MODULES=( dav dav_svn authz_svn )
REPOS_HTTPD_OWNER=( davtest_world_writable davtest_auth davtest_authz_anonymous )
REPOS=( "${REPOS_HTTPD_OWNER[@]}" svn_plus_ssh )

# {{{ helpers
_check_shell_settings() {
	opts="errexit nounset"
	# NOTE: when using this from scripts you always wan't to have these options on.
	# however, when testing fucntions by sourcing the lib, it's undesirable.
	# So here, we just print a warning.
	for i in $opts; do
		if set -o | grep $i | grep off; then
			echo "WARN: $i is off. You better set it on unless you know what you are doing" >&2
		fi
	done
}

_check_shell_settings

is_grp() {
	grep -qi ^$1: /etc/group
}
is_usr() {
	id $1 >/dev/null 2>&1
}
svn_cli_exe() {
	su ${SVN_CLI_USR} -c "$1" >$LOGF 2>&1
}
# }}}

svn_cleanup() {
	rc=$?

	_cleanup() {
		cd /tmp
		[ -n "${TMP_BASEDIR}" ] && rm -rf ${TMP_BASEDIR}

		[ -f "${SVN_APACHE_CONF_BAK}" ] && \
			mv $SVN_APACHE_CONF_BAK $SVN_APACHE_CONF

		is_usr $SVN_USR && userdel -r $SVN_USR >$LOGF 2>&1
		is_usr $SVN_CLI_USR && userdel -r $SVN_CLI_USR >$LOGF 2>&1
		is_grp $SVN_GRP && groupdel svn

		for i in ${APACHE_MODULES[@]}; do
			a2dismod $i
		done

		rcapache2 stop >$LOGF 2>&1
	}

	set +e
	_cleanup
	[ ! $? -eq 0 ] && echo "cleanup failed"

	for i in $RES_OK $RES_FAIL $RES_FAIL_INT $RES_FAIL_SETUP $RES_SKIPPED; do
		[ $rc = $i ] && return $rc
	done
	return $RES_FAIL_INT
}

svn_setup() {
	# Composed according to
	# https://bugzilla.novell.com/tr_list_cases.cgi?tags_type=anyexact&tags=packagename_subversion
	set -e

	# set LC_ALL, or we get::
	#
	#     svnadmin: error: cannot set LC_ALL locale
	#     svnadmin: error: environment variable LANG is not set
	#     svnadmin: error: please check that your locale name is correct
	#
	# with LC_ALL="" on SLE10SP4

	export LC_ALL="C"

	local key keygen pubkey pubkey_f auth_keys cmd

	is_grp $SVN_GRP || groupadd $SVN_GRP
	useradd -d $SVN_HOME -s /bin/bash -g $SVN_GRP $SVN_USR >$LOGF 2>&1

	is_usr $SVN_CLI_USR || \
		useradd -m -d $SVN_CLI_HOME -s /bin/bash $SVN_CLI_USR >$LOGF 2>&1

	mkdir -p $SVN_HOME/{repos,user_access,html,.ssh}
	su $SVN_CLI_USR -c "mkdir -p ${SVN_CLI_HOME}/.ssh"

	chown -R --no-dereference $SVN_USR:$SVN_GRP $SVN_HOME

	for i in ${REPOS[@]}; do
		su $SVN_USR -c "svnadmin create ${SVN_HOME}/repos/${i}"
	done

	[ -d "${SVN_CLI_HOME}/.ssh" ] && \
		[ ! $(ls ${SVN_CLI_HOME}/.ssh/ | wc -l) = "0" ] && \
		rm "${SVN_CLI_HOME}/.ssh/"*

	cmd="echo \"StrictHostKeyChecking no\" >> "
	cmd="${cmd} ${SVN_CLI_HOME}/.ssh/config"
	su $SVN_CLI_USR -c "$cmd"

	key="${SVN_CLI_HOME}/.ssh/id_rsa"
	keygen="ssh-keygen -t rsa -N \"\" -f ${key}"
	svn_cli_exe "$keygen"
	pubkey_f="${key}.pub"
	pubkey=$(cat $pubkey_f)

	auth_keys="command=\"svnserve -r ${SVN_HOME}/repos -t"
	auth_keys="${auth_keys} --tunnel-user=$SVN_CLI_USR\" ${pubkey}"
	echo "${auth_keys}" >> ${SVN_HOME}/.ssh/authorized_keys
	# {{{ make sure it is owned by properly
	# or get breakage when using umask 077
	chown ${SVN_USR} ${SVN_HOME}/.ssh/authorized_keys
	# }}}

	# extended
	# https://bugzilla.novell.com/tr_show_case.cgi?case_id=237918
	htpasswd2 -b -c ${SVN_HOME}/svn-test.passwd ${SVN_CLI_USR} testing \
		>$LOGF 2>&1

	cp ${SVN_APACHE_CONF} ${SVN_APACHE_CONF_BAK}

	for i in "${REPOS_HTTPD_OWNER[@]}"; do
		chown wwwrun:${SVN_GRP} -R ${SVN_HOME}/repos/$i
	done

	cp $SRCDIR/subversion.conf ${SVN_APACHE_CONF}

	for i in ${APACHE_MODULES[@]}; do
		a2enmod $i
	done

	rcapache2 restart >$LOGF 2>&1

	TMP_BASEDIR=`mktemp -d -t svn_test.XXX`

	# {{{ setup for dav+auth
		svn_pwd_dir=${SVN_CLI_HOME}/.subversion/auth/svn.simple
		mkdir -p $svn_pwd_dir
		chown ${SVN_CLI_USR} ${SVN_CLI_HOME}/.subversion -R
		realm=`grep FQDN_HOSTNAME ${SRCDIR}/svn-auth | sed "s/FQDN_HOSTNAME/$(hostname -f)/"`
		svn_pwd_file=$(echo "${realm}" | head -c-1 | md5sum | head -c 32)
		cp ${SRCDIR}/svn-auth $svn_pwd_dir/$svn_pwd_file
		sed -i "s/FQDN_HOSTNAME/$(hostname -f)/" $svn_pwd_dir/$svn_pwd_file
		len=$(hostname -f | wc -c)
		len=$(($len + 26)) # FIXME: magic value
		sed -i "s/REALM_LEN/${len}/" $svn_pwd_dir/$svn_pwd_file
		chown ${SVN_CLI_USR} $svn_pwd_dir/$svn_pwd_file
		chmod 600 $svn_pwd_dir/$svn_pwd_file
	# }}}

	# {{{ dav_authz
	cp ${SRCDIR}/authz-access-anonymous ${SVN_HOME}
	# }}}
}

_svn_version() {
	# Note: this generates Broken Pipe error on subversion < 1.7, this
	# is ok
	# see http://unix.stackexchange.com/questions/60222/why-does-subversion-give-a-broken-pipe-error-when-piped-into-head
	svn --version | head -n1 | sed 's/.* version \([^\s]\+\) .*/\1/'
}

_version_gt() {
	[ "$1" \> $2 ] && ! $(echo "$1" | grep "$2" -q)
}

_test() {
	local cmd wdir expected _diff reponame msg
	reponame=$(basename $CASE_URL) # beware

	test_import() {
		local import_tree
		if _version_gt $(_svn_version) "1.3" || \
		[ "${CASE_NAME}" = "SVN+SSH" ]; then
			import_tree=$source_tree;
		else
			# SLE10SP4 subversion (currenlty 1.3.1) is making a temp
			# file in the source path
			import_tree="$SVN_CLI_HOME/import_src"
			svn_cli_exe "mkdir $import_tree" || return $RES_FAIL_INT
			svn_cli_exe "cp $source_tree/* -r $import_tree"
		fi
		cmd="svn import $import_tree $CASE_URL -m \"import test\""
		svn_cli_exe "$cmd" || return $RES_FAIL;
	}

	test_checkout() {
		wdir="${CASE_BASEDIR}/commit"
		mkdir $wdir || return $RES_FAIL_INT
		chown $SVN_CLI_USR $TMP_BASEDIR -R || return $RES_FAIL_INT
		cd $wdir || return $RES_FAIL_INT
		svn_cli_exe "svn co ${CASE_URL}" || return $RES_FAIL
	}

	test_commit() {
		cd $reponame || return $RES_FAIL_INT
		svn_cli_exe "echo PASSED > README.test" || return $RES_FAIL_INT

		svn_cli_exe "svn add README.test" || return $RES_FAIL
		svn_cli_exe "svn commit -m testcommit" || return $RES_FAIL
		svn_cli_exe "svn cat README.test" || return $RES_FAIL
	}

	test_integrity() {
		wdir="${CASE_BASEDIR}/integrity"
		mkdir $wdir || return $RES_FAIL_INT
		chown $SVN_CLI_USR $wdir || return $RES_FAIL_INT
		cd $wdir || return $RES_FAIL_INT

		svn_cli_exe "svn co ${CASE_URL}" || return $RES_FAIL_INT
		cd ${wdir}/$reponame || return $RES_FAIL_INT

		repo_diff() {
			diff -x .svn -qNur $source_tree ${wdir}/$reponame
		}

		expected="Files ${source_tree}/README.test and"
		expected="${expected} ${wdir}/${reponame}/README.test differ"
		_diff=$(repo_diff)
		echo >$LOGF 2>&1
		[ $(echo ${_diff} | wc -l) = "1" ] && \
			[ "${_diff}" = "${expected}" ] || \
			return $RES_FAIL
	}

	subtest() {
		test_$1
		rc=$?
		[ $rc -eq $RES_OK ] && echo "$CASE_NAME: $2: PASSED" || \
			{ echo "$CASE_NAME: $2: FAILED"; return $rc; }
	}

	subtest import "Import test"
	subtest checkout "Checkout test"
	subtest commit "Commit test"
	subtest integrity "Checkout Integrity check"
}

# {{{ case definition
case_ssh() {
	export CASE_NAME="SVN+SSH"
	export CASE_URL="svn+ssh://${SVN_USR}@$svn_server/svn_plus_ssh/$reponame"
	export CASE_BASEDIR=${TMP_BASEDIR}/ssh
}

case_dav() {
	export CASE_NAME="DAV"
	export CASE_URL="http://$svn_server/repos/davtest_world_writable"
	export CASE_BASEDIR=${TMP_BASEDIR}/dav
}

case_dav_auth() {
	export CASE_NAME="DAV+AUTH"
	export CASE_URL="http://$svn_server/repos/davtest_auth"
	export CASE_BASEDIR=${TMP_BASEDIR}/dav_auth
}

case_dav_authz() {
	export CASE_NAME="DAV+AUTHZ"
	export CASE_URL="http://$svn_server/repos/davtest_authz"
	export CASE_BASEDIR=${TMP_BASEDIR}/dav_authz
}

case_null() {
	unset CASE_NAME CASE_URL CASE_BASEDIR
}

# }}}

test_case() {
	case_null
	case_$1

	mkdir $CASE_BASEDIR
	set +e
	_test
	rc=$?
	set -e
	[ $rc -eq 0 ] && echo "$CASE_NAME: PASSED" || echo "$CASE_NAME: FAILED"
	return $rc
}

svn_test_all() {
	usage() {
		echo "Usage: $0 <svn_server_fqdn> <local_dir> <case>"
		echo ""
		echo "<local_dir> is used for svn uploading"
		echo "if <case> is not given, it runs all cases"
	}

	main() {
		[ $# -lt 2 ] && { usage; exit 1; }

		local svn_server source_tree reponame cases

		svn_server="$1"
		source_tree="$2"

		reponame=$(basename $source_tree)

		echo "===$svn_server==="

		test_case $3
		rc=$?

		echo ""
		[ $rc -eq $RES_OK ] && echo "PASSED" || echo "FAILED"

		case $rc in
			0) ;;
			1) ;;
			*) rc=$RES_FAIL_INT;;
		esac

		return $rc
	}

	main $@
}
