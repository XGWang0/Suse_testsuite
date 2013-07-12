#!/bin/bash

# {{{ overridable config
LOGF=/dev/null
TMP_BASEDIR=
# }}}

# {{{ hardcoded config
SVN_GRP="svn"
SVN_USR="svn"
SVN_HOME="/srv/svn"

SVN_CLI_USR="svntest"
SVN_CLI_HOME="/home/svntest"

SVN_APACHE_CONF=/etc/apache2/conf.d/subversion.conf
SVN_APACHE_CONF_BAK="${SVN_APACHE_CONF}.bak"
# }}}

# {{{ test helpers
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
	cd /tmp
	[ -n "${TMP_BASEDIR}" ] && rm -rf ${TMP_BASEDIR}

	[ -f "${SVN_APACHE_CONF_BAK}" ] && \
		mv $SVN_APACHE_CONF_BAK $SVN_APACHE_CONF

	is_usr $SVN_USR && userdel -r $SVN_USR >$LOGF 2>&1
	is_usr $SVN_CLI_USR && userdel -r $SVN_CLI_USR >$LOGF 2>&1
	is_grp $SVN_GRP && groupdel svn

	a2dismod dav
	a2dismod dav_svn

	rcapache2 stop >$LOGF 2>&1
}

svn_setup() {
	# Composed according to
	# https://bugzilla.novell.com/tr_list_cases.cgi?tags_type=anyexact&tags=packagename_subversion

	local config key keygen pubkey pubkey_f auth_keys cmd

	config="./subversion.conf"

	is_grp $SVN_GRP || groupadd $SVN_GRP
	useradd -d $SVN_HOME -s /bin/bash -g $SVN_GRP $SVN_USR >$LOGF 2>&1

	is_usr $SVN_CLI_USR || \
		useradd -m -d $SVN_CLI_HOME -s /bin/bash $SVN_CLI_USR >$LOGF 2>&1

	mkdir -p $SVN_HOME/{repos,user_access,html,.ssh}
	su $SVN_CLI_USR -c "mkdir -p ${SVN_CLI_HOME}/.ssh"

	chown -R --no-dereference $SVN_USR:$SVN_GRP $SVN_HOME

	su $SVN_USR -c "svnadmin create ${SVN_HOME}/repos/svn_plus_ssh"
	su $SVN_USR -c "svnadmin create ${SVN_HOME}/repos/davtest_world_writable"
	su $SVN_USR -c "svnadmin create ${SVN_HOME}/repos/davtest_auth"

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

	# extended
	# https://bugzilla.novell.com/tr_show_case.cgi?case_id=237918
	htpasswd2 -b -c ${SVN_HOME}/svn-test.passwd ${SVN_CLI_USR} testing \
		>$LOGF 2>&1

	cp ${SVN_APACHE_CONF} ${SVN_APACHE_CONF_BAK}

	chown wwwrun:${SVN_GRP} -R \
		${SVN_HOME}/repos/{davtest_world_writable,davtest_auth}

	cp $config ${SVN_APACHE_CONF}

	a2enmod dav
	a2enmod dav_svn

	rcapache2 restart >$LOGF 2>&1

	TMP_BASEDIR=`mktemp -d -t svn_test.XXX`
}

_test() {
	set -e
	local cmd wdir expected _diff reponame
	reponame=$(basename $CASE_URL) # beware

	# {{{
	cmd="svn import $source_tree $CASE_URL -m \"import test\""
	svn_cli_exe "$cmd"
	echo "$CASE_NAME: Import test: PASSED"
	# }}}

	# {{{
	wdir="${CASE_BASEDIR}/commit"
	mkdir $wdir
	chown $SVN_CLI_USR $TMP_BASEDIR -R
	cd $wdir
	svn_cli_exe "svn co ${CASE_URL}"

	echo "$CASE_NAME: Checkout test: PASSED"
	# }}}

	# {{{
	cd $reponame
	svn_cli_exe "echo PASSED > README.test"

	svn_cli_exe "svn add README.test"
	svn_cli_exe "svn commit -m testcommit"
	svn_cli_exe "svn cat README.test"

	echo "$CASE_NAME: Commit test: PASSED"
	# }}}

	# {{{
	wdir="${CASE_BASEDIR}/integrity"
	mkdir $wdir
	chown $SVN_CLI_USR $wdir
	cd $wdir

	svn_cli_exe "svn co ${CASE_URL}"
	cd ${wdir}/$reponame

	repo_diff() {
		diff -x .svn -qNur $source_tree ${wdir}/$reponame
	}

	expected="Files ${source_tree}/README.test and"
	expected="${expected} ${wdir}/${reponame}/README.test differ"
	_diff=$(repo_diff) || true
	echo >$LOGF 2>&1
	[ $(echo ${_diff} | wc -l) = "1" ] && \
		[ "${_diff}" = "${expected}" ] || \
		return 1

	echo "$CASE_NAME: Checkout Integrity check: PASSED"
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

	# {{{
		svn_pwd_dir=${SVN_CLI_HOME}/.subversion/auth/svn.simple
		mkdir -p $svn_pwd_dir
		chown ${SVN_CLI_USR} ${SVN_CLI_HOME}/.subversion -R
		realm=`grep FQDN_HOSTNAME ${CURDIR}/$(dirname $0)/svn-auth | sed "s/FQDN_HOSTNAME/$(hostname -f)/"`
		svn_pwd_file=`python -c "import hashlib; print hashlib.md5(\"${realm}\").hexdigest()"`
		cp ${CURDIR}/$(dirname $0)/svn-auth $svn_pwd_dir/$svn_pwd_file
		sed -i "s/FQDN_HOSTNAME/$(hostname -f)/" $svn_pwd_dir/$svn_pwd_file
		len=$(hostname -f | wc -c)
		len=$(($len + 26)) # FIXME: magic value
		sed -i "s/REALM_LEN/${len}/" $svn_pwd_dir/$svn_pwd_file
		chown ${SVN_CLI_USR} $svn_pwd_dir/$svn_pwd_file
		chmod 600 $svn_pwd_dir/$svn_pwd_file
	# }}}
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
		echo "Usage: $0 <svn_server_fqdn> <local_dir>"
		echo ""
		echo "<local_dir> is used for svn uploading"
	}

	main() {
		[ $# -lt 2 ] && { usage; exit 1; }

		local CURDIR svn_server source_tree reponame

		svn_server="$1"
		source_tree="$2"

		CURDIR=`pwd`

		reponame=$(basename $source_tree)

		echo "===$svn_server==="

		rc=0
		for i in ssh dav dav_auth; do
			set +e
			test_case $i
			rc=$(($rc | $?))
			set -e
		done

		echo ""
		[ $rc -eq 0 ] && echo "PASSED" || echo "FAILED"

		return $rc
	}

	main $@
}
