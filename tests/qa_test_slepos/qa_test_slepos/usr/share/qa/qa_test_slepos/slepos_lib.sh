#!/bin/bash -x
# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************


VERSION=0.5


###############################################################
# Initialization
###############################################################

CONF_PATH=/usr/share/qa/qa_test_slepos
SLEPOS_LIB_FILE=/root/slepos_lib.sh
LOCAL_CONFIG=/root/qa_slepos-local_config.sh

# am I sourced?
unset is_sourced
if [ "$0" = '/bin/bash' ] || [ "$0" = '-bash' ] || [ "$0" = 'bash' ]; then
	is_sourced=yes
fi

# now should be defined on_admin/on_branch/on_image variables
source "$CONF_PATH"/role_and_version_detection.sh

source "$CONF_PATH/defaults.sh"
if [ "$CONFIG_EDITED" = no ]; then
	echo "Edit local configuration first, please."
	echo "It is in /usr/share/qa/qa_test_slepos/local_config.sh or its symlink /root/qa_slepos-local_config.sh."
	if [ "$is_sourced" ]; then
		return $INT_ERROR_CODE
	else
		exit $INT_ERROR_CODE
	fi
fi

GREEN="\033[01;32m"
YELLOW="\033[01;33m"
RED="\033[01;31m"
MAGENTA="\033[01;35m"
CYAN="\033[01;36m"
BOLD="\033[01;1m"
NONE="\033[00m"

###
# return codes for corect handling by ctcs2
####

# success code
SUCCESS_CODE=0

# normal error code
ERROR_CODE=1

# internal error code
INT_ERROR_CODE=11

# skipped code
SKIPPED_CODE=22

# request for kill - immediately terminate
KILL_CODE=255


###############################################################
# Generic functions
###############################################################


info() {
	echo -e "${GREEN}$1${NONE}"
}

error() {
	echo -e "${RED}$1${NONE}"
}

error_internal() {
	echo -e "${MAGENTA}$1${NONE}"
}

warn() {
	echo -e "${CYAN}$1${NONE}"
}

workaround() {
	echo -e "${YELLOW}Workaround warning: $1${NONE}"
}


firewall_ports() {
	# enable ports on firewall (check local_config.sh), NLPOS 9 doesn't support it
	if [ "$pos_version" != 9 ]; then
		for port in ${!1}; do
			yast2 firewall services add tcpport=$port udpport=$port zone=EXT
    		done
	fi
}


# NOTE: this is not used yet

do_base_check() {
# this can have temporary files as parameters
# if something goes wrong, these files are not deleted

	case $? in
		0)	if [ "${*}" ]; then
				echo "Removing unneeded files..."
				rm -f "${@}"
				echo "Removed."
			fi
			echo "Exiting..."
			return $SUCCESS_CODE ;;
		1)	return $ERROR_CODE ;;
		*)	return $INT_ERROR_CODE ;;
	esac
}

unwrap_ldap() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# ldapsearch produces output with fixed length of the line
# this sed code make from multi-line record (where other lines begins with spaces)
# single-line record
	sed ':a; $!N;s/\n //;ta;P;D' "${1:-/dev/stdin}"
}

#######
# LDAP low-level stuff
#######

if [ -z "$is_sourced" ] || [ "$on_admin" ]; then

create_scServerContainer() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scServerContainer \
			--cn "${scServerContainer}"
}


create_scBranchserver() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scBranchServer \
			--cn "${scBranchServer}" \
			${scRefServerDn:+--scRefServerDn "$scRefServerDn"} \
			${scPubKey:+--scPubKey "$scPubKey"}
}

create_scLocation() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	if [ ${pos_version}x = 11x ]; then
		userPasswordOption="--userPassword $userPassword"
	else
		unset userPasswordOption
	fi
	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
		--scLocation \
			--cn "${scLocation}" \
			--ipNetworkNumber "${network}" \
			--ipNetmaskNumber "${mask}" \
			--scDhcpRange "${DhcpRange1},${DhcpRange2}" \
			--scDhcpFixedRange "${DhcpFixedRange1},${DhcpFixedRange2}" \
			--scDefaultGw "${gateway}" \
			--scDynamicIp "${DynamicIP}" \
			--scWorkstationBaseName "${WorkstationBaseName}" \
			--scEnumerationMask "${EnumerationMask}" \
			--scDhcpExtern "${dhcpExtern}" \
			${userPasswordOption} \
			${scLdapDn:+--scLdapDn "$scLdapDn"} \
			${scDnsDn:+--scDnsDn "$scDnsDn"} \
			${scPrinterBaseName:+--scPrinterBaseName "$scPrinterBaseName"} \
			${associatedDomain:+--associatedDomain "$associatedDomain"}
}

create_scNetworkcard() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
		--scNetworkcard \
			--scDevice "${device}" \
			--ipHostNumber "${internal_ip}" \
			${macAddress:+--macAddress "$macAddress"} \
			${scModul:+--scModul "$scModul"} \
			${scModulOption:+--scModulOption "$scModulOption"} \
			${ipNetmaskNumber:+--ipNetmaskNumber "$ipNetmaskNumber"}
}

create_scPosimage() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--base "cn=global,o=${organization},c=${country}" \
		--add \
			--scPosImage \
			--cn "${cn}" \
			--scImageName "${image_name}" \
			--scPosImageVersion "${image_version}" \
			--scDhcpOptionsRemote "${dhcp_opts_remote}" \
			--scDhcpOptionsLocal "${dhcp_opts_local}" \
			--scImageFile "${image_file}" \
			--scBsize "${bsize}" \
			${config_file:+--scConfigFile "$config_file"}
}

remove_scPosimage() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--remove \
			--DN "${dn}"
}

create_scPosimage_in_container() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--base "cn=${container},o=${organization},c=${country}" \
		--add \
			--scPosImage \
			--cn "${cn}" \
			--scImageName "${image_name}" \
			--scPosImageVersion "${image_version}" \
			--scDhcpOptionsRemote "${dhcp_opts_remote}" \
			--scDhcpOptionsLocal "${dhcp_opts_local}" \
			--scImageFile "${image_file}" \
			--scBsize "${bsize}" \
			${config_file:+--scConfigFile "$config_file"}
}

create_scDistributionContainer() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--base "cn=global,o=${organization},c=${country}" \
		--add \
			--scDistributionContainer \
			--cn "${cn}" \
			--scKernelName "${kernel_name}" \
			--scKernelVersion "${kernel_version}" \
			--scKernelMatch "${kernel_match}" \
			--scInitrdName "${initrd_name}" \
			${kernel_expression:+--scKernelExpression "$kernel_expression"}
}

create_scCashRegister() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
	    --base "cn=global,o=${organization},c=${country}" \
	    --add \
		--scCashRegister \
		--cn "${cr}" --scCashRegisterName "${cr_name}" \
		${scPosImageDn:+--scPosImageDn "${scPosImageDn}"} \
		${scPosDeltaImageDn:+--scPosDeltaImageDn "${scPosDeltaImageDn}"} \
		${scDiskJournal:+--scDiskJournal "${scDiskJournal}"}

 # FIXME --scPosImageDn "cn=${image},cn=global,o=${organization},c=${country}"
}

create_scRamDisk() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--base "cn=${cr},cn=global,o=${organization},c=${country}" \
		--add \
			--scRamDisk \
			--cn "${disk_device_name}" --scDevice "${disk_device}"
}

create_scHarddisk() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--base "cn=${cr},cn=global,o=${organization},c=${country}" \
		--add \
			--scHarddisk \
			--cn "${disk_device_name}" --scDevice "${disk_device}" --scHdSize "${disk_size}" \
			--scPartitionsTable "${disk_partitioning}"
}

create_tftp_service() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scService \
			--cn tftp \
			--ipHostNumber "${internal_ip}" \
			--scDnsName tftp \
			--scServiceName tftp \
			--scServiceStartScript atftpd \
			--scServiceStatus TRUE
}

create_dhcp_service() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scService \
			--cn dhcp \
			--ipHostNumber "${internal_ip}" \
			--scDnsName dhcp \
			--scServiceName dhcp \
			--scServiceStartScript dhcpd \
			--scServiceStatus TRUE \
			${scServiceEmail:+--scServiceEmail "$scServiceEmail"}

}

create_dns_service() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scService \
			--cn dns \
			--ipHostNumber "${internal_ip}" \
			--scDnsName dns \
			--scServiceName dns \
			--scServiceStartScript named \
			--scServiceStatus TRUE \
			${scServiceEmail:+--scServiceEmail "$scServiceEmail"}
}

create_OU() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "o=${organization},c=${country}" \
		--add \
			--organizationalUnit \
			--ou "${organizationalUnit}" \
			${organizationalUnitDesc:+--description "$organizationalUnitDesc"}
}

create_scWorksctation() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
		--add \
			--scWorkstation \
			--macAddress "${macAddress}" \
			--ipHostNumber "${ipHostNumber}" \
			${scSerialNumber:+--scSerialNumber "$scSerialNumber"} \
			${scRefPcDn:+--scRefPcDn "$scRefPcDn"} \
			${scPosImageDn:+--scPosImageDn "$scPosImageDn"} \
			${scPosDeltaImageDn:+--scPosDeltaImageDn "$scPosDeltaImageDn"} \
			${scPosImageVersion:+--scPosImageVersion "$scPosImageVersion"} \
			${scPosRegisterBiosVersion:+--scPosRegisterBiosVersion "$scPosRegisterBiosVersion"} \
			${scPosRegisterType:+--scPosRegisterType "$scPosRegisterType"} \
			${scConfigFileDn:+--scConfigFileDn "$scConfigFileDn"} \
			${scStandardPrinterDn:+--scStandardPrinterDn "$scStandardPrinterDn"} \
			${scStandardPrinter:+--scStandardPrinter "$scStandardPrinter"} \
			${scImageVersion:+--scImageVersion "$scImageVersion"} \
			${scPosGroupDn:+--scPosGroupDn "$scPosGroupDn"} \
			${scDiskJournal:+--scDiskJournal "$scDiskJournal"} \
			${scConfigUpdate:+--scConfigUpdate "$scConfigUpdate"} \
			${scNotifiedImage:+--scNotifiedImage "$scNotifiedImage"}
}

assign_image_to_workstation() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	# version is 3.1.5 (for example) only. No ';active' no 'delta' here.

# Assigning an Image to a Point of Service Terminal
# parameters are not needed
#	$1	whole scWorkstation DN (cn=CR01,...)
#	$2	DN of image to be used
#	$3	image version
	(
		if [ $# -lt 2 ]; then
			error "assign_image_to_workstation() needs at least 2 arguments"
			handle_help "$FUNCNAME"
			return $INT_ERROR_CODE
		fi

		if grep "o=${organization},c=${country}" <<< "$1" ; then
			DN="$1"
			CR_NAME="${1%%,*}"
		else
			CR_NAME="$1"
			DN="`ldap_search cn="$1" | grep dn | cut -d\  -f2`"
			[ `wc -l <<< "$DN"` -ne 1 ] && { error "$1 not recognized uniquely, found: $DN" ; return $INT_ERROR_CODE; }
		fi
		
		info "Workstation DN: $DN"

		if grep "o=${organization},c=${country}" <<< "$2" ; then
			scPosImageDn="$2"
		else
			scPosImageDn="`ldap_search cn="$2" | grep dn | cut -d\  -f2`"
			[ `wc -l <<< "$scPosImageDn"` -ne 1 ] && { error "$2 not recognized uniquely, found: $scPosImageDn" ; return $INT_ERROR_CODE; }
		fi

		info "Image DN: $scPosImageDn"

		if [ "$3" ]; then
			scPosImageVersion="$3"
		else
			# lets try to find it out from LDAP_OUT
			scPosImageVersion="`ldap_search cn="$CR_NAME" | sed -n 's/scPosImageVersion: //p'`"
		fi

		info "Image version: $scPosImageVersion"

		show_log_on_fail "modify_scWorkstation" || { error "modify_scWorkstation failed ($DN)"; return $ERROR_CODE; }

		# remove files to rerun detection again
		MAC="`ldap_search cn="$CR_NAME" | grep macAddress | cut -d\  -f2 | sed 's/:/\\:/g'`"
		LOCATION="`ldap_search cn="$CR_NAME" | sed -n 's/^dn: //p' | cut -d, -f2,3,4,5`"
		ELEMENTS="$(ldap_search | grep "cn=[^,]*,cn=[^,]*,$LOCATION" | sed -n 's/^dn: cn=\([^,]*\),.*/\1/p')"
		for element in $ELEMENTS; do
			if ldap_search "cn=$element" | grep "objectClass: scBranchServer" &> /dev/null; then
				BRANCH_NAME="$element"
			fi
		done
#		BRANCH_NAME="$(ldap_search | grep "cn=[^,]*,cn=[^,]*,$LOCATION" | sed -n 's/^dn: cn=\([^,]*\),.*/\1/p' | while read element; do if ldap_search "cn=$element" | grep "objectClass: scBranchServer" &> /dev/null; then echo "$element" ; fi ; done)"
		ssh root@"$BRANCH_NAME" "$SLEPOS_LIB_FILE remove_cr_conf \"$MAC\""
	)
}

modify_scWorkstation() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl --user "cn=${admin},o=${organization},c=${country}" --password "${pass}" \
		--modify \
			--scWorkstation \
			--DN "${DN}" \
			${scPosImageVersion+--scPosImageVersion "${scPosImageVersion}"} \
			${scPosImageDn:+--scPosImageDn "${scPosImageDn}"}

			#${scImageName:+--scImageName "${image_name}"} \
			#${scPosImageVersion+--scPosImageVersion "${scPosImageVersion}"} \
			#${scDhcpOptionsRemote+--scDhcpOptionsRemote "${dhcp_opts_remote}"} \
			#${scDhcpOptionsLocal+--scDhcpOptionsLocal "${dhcp_opts_local}"} \
			#${scImageFile+--scImageFile "${image_file}"} \
			#${scBsize+--scBsize "${bsize}"} \
			#${config_file:+--scConfigFile "$config_file"}
			
			#${cn:+--cn "${cn}"} \


			# ${scPosImageVersion+--scPosImageVersion "${image_version}"} \
			# ${scPosImageVersion+--scPosImageVersion "${scPosImageVersion}"} \

			#This works:
			# posAdmin.pl --user cn=admin,o=PrazskeKanalizace,c=pl --password root --modify --scWorkstation --DN cn=CR01,cn=GrandKanal,ou=vinohrady,o=PrazskeKanalizace,c=pl --scPosImageVersion '3.1.5.delta;active' --scPosImageDn cn=mini,cn=default,cn=global,o=PrazskeKanalizace,c=pl

}

modify_scCashRegister() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	# posAdmin.pl --user cn=admin,o=PrazskeKanalizace,c=pl --password root --modify --scCashRegister --scPosImageDn cn=miniyebo,cn=default,cn=global,o=PrazskeKanalizace,c=pl --DN cn=default_CR,cn=global,o=PrazskeKanalizace,c=pl
	#it returns fail, but it modifies ldap ... strange thing ...
	##Parsing options:
	##
	## base action: --modify
	## item : 'scCashRegister'
	##
	## action = 'modify':
	##
	##    scPosImageDn:                cn=minikkt,cn=default,cn=global,o=PrazskeKanalizace,c=pl
	##    password:                    ********
	##    user:                        cn=admin,o=PrazskeKanalizace,c=pl
	##    DN:                          cn=default_CR,cn=global,o=PrazskeKanalizace,c=pl
	##    scCashRegister:
	##
	##Invoking apply:
	##
	##applying modifications in scCashRegister of cn=default_CR,cn=global,o=PrazskeKanalizace,c=pl
	##  --scPosImageDn "cn=minikkt,cn=default,cn=global,o=PrazskeKanalizace,c=pl" => "cn=miniyebo,cn=default,cn=global,o=PrazskeKanalizace,c=pl"
	##
	##Error in LDAP access (80: commit failed
	##
	##Operation failed.
	##hitman:~ # echo "$?"
	##1


	# TODO: add branch server variant

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--modify --scCashRegister \
			${scPosImageDn:+--scPosImageDn "$scPosImageDn"} \
			${scCashRegisterName:+--scCashRegisterName "$scCashRegisterName"} \
			--DN "${DN}"
}

modify_scPosImage() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--modify --scPosImage \
			${scPosImageDn:+--scPosImageDn "$scPosImageDn"} \
			${scPosImageVersion:+--scPosImageVersion "$scPosImageVersion"} \
			${scImageFile:+--scImageFile "$scImageFile"} \
			--DN "${DN}"
}

set_default_image() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

#	$1	name of image, which should be default

	# posAdmin.pl --user cn=admin,o=PrazskeKanalizace,c=pl --password root --modify --scCashRegister --scPosImageDn cn=miniyebo,cn=default,cn=global,o=PrazskeKanalizace,c=pl --DN cn=default_CR,cn=global,o=PrazskeKanalizace,c=pl
	# it returns fail, but it modifies LDAP ... strange thing ...
	# see modify_scCashRegister

	# TODO: add branch server variant

	(
		DN="$( ldap_search scCashRegisterName | sed 's/^dn: /#/' | tr '#\n' '\n#' | grep 'scCashRegisterName: default' | sed 's/#.*//' )"

		[ -z "$DN" ] && { echo "scCashRegister object with scCashRegisterName attribute with value 'default' hasn't been found"; return $INT_ERROR_CODE; }
		info "Changing DN ${DN}"
		
		[ -z "$1" ] && { echo "The name of image is needed as parameter. For example 'minimal'."; return $INT_ERROR_CODE; }

		scPosImageDn="cn=$1,cn=default,cn=global,o=${organization},c=${country}"
		modify_scCashRegister
	)

	info "/srv/tftpboot/KIWI/config.* on BS should be erased to apply changes."
}

change_image_version() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

#	$1	name of image, which should have changed version
#	$2	new version

	# posAdmin.pl --user cn=admin,o=PrazskeKanalizace,c=pl --password root --modify --scCashRegister --scPosImageDn cn=miniyebo,cn=default,cn=global,o=PrazskeKanalizace,c=pl --DN cn=default_CR,cn=global,o=PrazskeKanalizace,c=pl
	# it returns fail, but it modifies LDAP ... strange thing ...
	# see modify_scCashRegister

	# TODO: add branch server variant

###                        ${scPosImageDn:+--scPosImageDn "$scPosImageDn"} \
###                        ${scPosImageVersion:+--scPosImageVersion "$scPosImageVersion"} \
###                        --DN "${DN}"



	(
		DN="$( ldap_search "$1" | grep "^dn: cn=$1,cn=" | sed 's/^dn: //' )"

		[ -z "$DN" ] && { echo "Image $1 hasn't been found"; return $INT_ERROR_CODE; }
		info "Changing DN ${DN}"
		
		[ -z "$1" ] && { echo "The name of image is needed as parameter. For example 'minimal'."; return $INT_ERROR_CODE; }

		#scPosImageDn="cn=$1,cn=default,cn=global,o=${organization},c=${country}"
		scPosImageVersion="$2"
		modify_scPosImage
	)
}

change_image_file() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

#	$1	name of image, which should have changed version
#	$2	new file

	(
		DN="$( ldap_search "$1" | grep "^dn: cn=$1,cn=" | sed 's/^dn: //' )"

		[ -z "$DN" ] && { echo "Image $1 hasn't been found"; return $INT_ERROR_CODE; }
		info "Changing DN ${DN}"
		
		[ -z "$1" ] && { echo "The name of image is needed as parameter. For example 'minimal'."; return $INT_ERROR_CODE; }

		#scPosImageDn="cn=$1,cn=default,cn=global,o=${organization},c=${country}"
		scImageFile="$2"
		modify_scPosImage
	)
}

# NOTE: not used yet
check_output() {
#	$1	supposed output
#	$2	LDAP output


	diff "$1" <(unwrap_ldap "$2") | wc -l
	do_base_check "$1" "$2"
}

# NOTE: not used yet
test_dhcp_service() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

# This function is relict - it's not used anywhere yet
	LDAP_OUT="`mktemp "$FUNCNAME-ldap.XXX"`"
	SUPPOSED_OUT="`mktemp "$FUNCNAME-supposed.XXX"`"
	ldap_search "cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation}" "cn=dhcp" > "$LDAP_OUT"

	echo "dn: cn=dhcp,cn=${scBranchServer},cn=${scServerContainer},cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}
	scServiceName: dhcp
	scServiceStatus: TRUE
	scDnsName: dhcp
	scServiceStartScript: dhcpd
	cn: dhcp
	objectClass: scService
	objectClass: top
	ipHostNumber: ${internal_ip}
	" > "$SUPPOSED_OUT"
	check_output "$SUPPOSED_OUT" "$LDAP_OUT"
}

fi # end of admin server namespace

ldap_search() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1	LDAP query
#	$2	base used for LDAP query (without organization and country)
	BASE="${2:+$2,}"
	ldapsearch -H $LDAP_SERVER -LLL -x -w "${pass}" \
		-D "cn=${admin},o=${organization},c=${country}" \
		-b "${BASE}o=${organization},c=${country}" \
		${1:+"$1"} | unwrap_ldap
}

if [ -z "$is_sourced" ] || [ "$on_branch" ]; then

remove_cr_conf() {
	rm -v "$BRANCH_IMAGE_PATH/../upload/"*"$1" "${BRANCH_IMAGE_PATH}/../CR/"*"$1"
}

ldap_search_branch() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1	LDAP query
#	$2	base used for LDAP query (without organization and country)
	(
		read_branch_server_config
		BASE="${2:+$2,}"
		ldapsearch -H "ldap://localhost" -LLL -x -w "${userPassword}" \
			-D "cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
			-b "${BASE}cn=${scLocation},ou=${organizationalUnit},o=${organization},c=${country}" \
			"$1" | unwrap_ldap
	)
}

fi

########
# LDAP high-level stuff
########

if [ -z "$is_sourced" ] || [ "$on_admin" ]; then
# NOTE: on admin server just add it directly to LDAP database
add_image_to_ldap() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	(
		cn="$1"
		image_name="$1"
		FILENAME="$(basename `ls "$SYSTEM_IMAGE_TARGET_PATH/$1"* | sort | head -n 1`)"
		if [ "$pos_version" -eq 9 ]; then
			image_version="${FILENAME#${FILENAME%-*-*-*-*}-};active"
		else
			image_version="${FILENAME##*-};active"
		fi
		image_file="${FILENAME%-*}"
		dhcp_opts_remote="/boot/pxelinux.0"
		dhcp_opts_local="LOCALBOOT"
		bsize=8192
		# now we have enough informations about image
		show_log_on_fail "create_scPosimage" || { error "add_image_to_ldap failed ($1)"; return $ERROR_CODE; }
	)
	info "You'll probably need to run possyncimages from BS now."
}

else # on_admin?
# NOTE: if I'm not on admin server, I call it remotely
add_image_to_ldap() {
	ssh root@"$admin_server_name" "$SLEPOS_LIB_FILE add_image_to_ldap $1"
}

fi # on_admin?

if [ -z "$is_sourced" ] || [ "$on_admin" ]; then
# NOTE: on admin server just add it directly to LDAP database
del_image_from_ldap() {
	
	#non-working !!!!!!
	#this works: posAdmin.pl --user cn=admin,o=PrazskeKanalizace,c=pl --password root --remove --DN 'cn=mini,cn=default,cn=global,o=PrazskeKanalizace,c=pl'
	
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	(
		cn="$1"
		# find whole DN of image to be deleted
		dn="$(ldap_search "$cn" | sed -n 's/^dn: \(.*\)/\1/p')"
		# now we have enough informations about image
		show_log_on_fail "remove_scPosimage" || { error "del_image_from_ldap failed ($1)"; return $ERROR_CODE; }
	)
}

else # on_admin?
# NOTE: if I'm not on admin server, I call it remotely
del_image_from_ldap() {
	ssh root@"$admin_server_name" "$SLEPOS_LIB_FILE del_image_from_ldap $1"
}

fi # on_admin?


if [ -z "$is_sourced" ] || [ "$on_admin" ]; then
# NOTE: on admin server just add it directly to LDAP database
add_image_to_ldap_in_container() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	(
		#$1 name of image
		#$2 name of container
		cn="$1"
		image_name="$1"
		FILENAME="$(basename `ls "$SYSTEM_IMAGE_TARGET_PATH/$1"* | sort | head -n 1`)"
		if [ "$pos_version" -eq 9 ]; then
			image_version="${FILENAME#${FILENAME%-*-*-*-*}-};active"
		else
			image_version="${FILENAME##*-};active"
		fi
		image_file="${FILENAME%%-*}"
		dhcp_opts_remote="/boot/pxelinux.0"
		dhcp_opts_local="LOCALBOOT"
		bsize=8192
		container="$2"
		# now we have enough informations about image
		show_log_on_fail "create_scPosimage_in_container" || { error "add_image_to_ldap_in_container failed ($1)"; return $ERROR_CODE; }
	)
}

else # on_admin?
# NOTE: if I'm not on admin server, I call it remotely
add_image_to_ldap_in_container() {
	ssh root@"$admin_server_name" "$SLEPOS_LIB_FILE add_image_to_ldap_in_container $1"
}

fi # on_admin?

if [ -z "$is_sourced" ] || [ "$on_admin" ]; then
# NOTE: on admin server just add it directly to LDAP database
add_container_to_ldap() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	(
		#$1 container name
		#$2 kernel name
		#$3 kernel version
		#$4 initrd name
		cn="$1"
		kernel_name="$2"
		kernel_version="$3"
		kernel_match="MATCH_VERSION"; #don't know if there is differrent option avaiable
		initrd_name="$4"
		# now we have enough informations about container
		show_log_on_fail "create_scDistributionContainer" || { error "add_container_to_ldap failed ($1)"; return $ERROR_CODE; }
	)
}

else # on_admin?
# NOTE: if I'm not on admin server, I call it remotely
add_container_to_ldap() {
	ssh root@"$admin_server_name" "$SLEPOS_LIB_FILE add_container_to_ldap $1"
}

fi # on_admin?

# this belongs to admin server namespace
if [ -z "$is_sourced" ] || [ "$on_admin" ]; then

run_posInitLdap() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	if [ "$1" = -x ]; then
		COMMAND="bash -x posInitLdap.sh"
	else
		COMMAND="posInitLdap.sh"
	fi

	# fix non-interactivity of the script
	fix_posReadPassword

	{
		echo "${organization}"
		echo "${country}"
		echo "${pass}"
		echo "${pass}"
		echo "${ssl}"
		# "THIS WILL DELETE ALL DATA IN THE LDAP DATABASE!" - press Enter
		echo ""
	} | $COMMAND
	do_base_check
}

create_database() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# this will create all objects in database
	info "Creating all organizational units"
	# Comment: I use 'ls' to be sure, if this file does not exist
	#          for cycle will not be run even once
	for i in `ls $CONF_PATH/organizational_unit* 2> /dev/null`; do
		(
			source $i
			show_log_on_fail "create_OU" || { error "create_OU failed ($i)"; return $ERROR_CODE; }
		)
	done

	info "Creating all locations"
	for i in `ls $CONF_PATH/location* 2> /dev/null`; do
		(
			source $i
			show_log_on_fail "create_scLocation" || { error "create_scLocation failed ($i)"; return $ERROR_CODE; }
		)
	done

	info "Creating all branch servers with network cards and dhcp, tftp services"
	if [ "$branch_server_list" ]; then
		for i in $branch_server_list; do
			(
				read_branch_server_config "$i"
				scBranchServer="$i"
				show_log_on_fail "create_scServerContainer" || { error "create_scServerContainer failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_scBranchserver" || { error "create_scBranchserver failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_scNetworkcard" || { error "create_scNetworkcard failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_dhcp_service" || { error "create_dhcp_service failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_tftp_service" || { error "create_tftp_service failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_dns_service" || { error "create_dns_service failed ($i)"; return $ERROR_CODE; }
			)
			RES="$?"
			if [ "$RES" -ne 0 ]; then
				if [ "$is_sourced" ]; then
					return "$RES"
				else
					exit "$RES"
				fi
			fi
		done
	else
		for i in "$CONF_PATH"/branch_server-*sh; do
			(
				source "$i"
				show_log_on_fail "create_scServerContainer" || { error "create_scServerContainer failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_scBranchserver" || { error "create_scBranchserver failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_scNetworkcard" || { error "create_scNetworkcard failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_dhcp_service" || { error "create_dhcp_service failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_tftp_service" || { error "create_tftp_service failed ($i)"; return $ERROR_CODE; }
				show_log_on_fail "create_dns_service" || { error "create_dns_service failed ($i)"; return $ERROR_CODE; }
			)
		done
	fi
	unset BRANCH_SERVER_LIST

	info "Creating all POS machines"
	for i in `ls $CONF_PATH/machine* 2> /dev/null`; do
		(
			source $i
			show_log_on_fail "create_scCashRegister" || { error "create_scCashRegister failed ($i)"; return $ERROR_CODE; }
			case "$disk_type" in
				"disk")
					show_log_on_fail "create_scHarddisk" || { error "create_scHarddisk failed ($i)"; return $ERROR_CODE; } ;;
				"ramdisk")
					show_log_on_fail "create_scRamDisk" || { error "create_scRamDisk failed ($i)"; return $ERROR_CODE; } ;;
				*)
					error "Unsupported disk type" ;;
			esac
			
		)
	done
}

fi # end of admin namespace

# this belongs to branch server namespace
if [ -z "$is_sourced" ] || [ "$on_branch" ]; then

read_branch_server_config() {
	HOST="${1:-"$HOSTNAME"}"
	i="$1"
	HOST="${HOST//-/_}"
	if [ -f "$BRANCH_SERVER_CONFIG" ]; then
		 source "$BRANCH_SERVER_CONFIG"
	else
		# usualy branch server configuration file sources also location file
		# we don't have one so we do it now
		# read location and information about above LDAP structure
		eval HOSTNAME_location="\"\$${HOST}_location\""
		if [ "${HOSTNAME_location}" ]; then
			source "$CONF_PATH/location${HOSTNAME_location}.sh"
		else
			source "$CONF_PATH/location$location_default.sh"
		fi
	fi

	# set branch server from variables

	# IP address of internal network	
	eval HOSTNAME_internal_ip="\"\$${HOST}_internal_ip\""
	if [ "${HOSTNAME_internal_ip}" ]; then
		inernal_ip="${HOSTNAME_internal_ip}"
	fi
	if [ -z "$internal_ip" ]; then
		internal_ip="$default_internal_ip"
	fi

	# network interface used for internal network defined directly
	if eval test "\"\${${HOST}_internal_device}\""; then
		eval device="\"\${${HOST}_internal_device}\""
	fi

	# or defined by MAC address
	if [ -z "$device" ] && eval test "\"\${${HOST}_internal_mac}\""; then
		device="`eval find_interface_by_mac $i "\"\${${HOST}_internal_mac}\""`"
	fi

	# if none of that is defined - last try - autodetection
	if [ -z "$device" ]; then
		device="`find_the_other_interface $i`"
	fi
	
	if [ -z "$device" ]; then
		error_internal "Branch server '$HOST' doesn't have properly set internal network interface."
		if [ "$is_sourced" ]; then
			return $INT_ERROR_CODE
		else
			exit $INT_ERROR_CODE
		fi
	fi

	if [ -z "$scLocation" ]; then
		error_internal "Something weird happened with location configuration for branch server '$HOST'."
		if [ "$is_sourced" ]; then
			return $INT_ERROR_CODE
		else
			exit $INT_ERROR_CODE
		fi
	fi
}

run_posInitBranchserver() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	if [ "$1" = -x ]; then
		COMMAND="bash -x posInitBranchserver.sh"
	else
		COMMAND="posInitBranchserver.sh"
	fi
	fix_posReadPassword
	(
		read_branch_server_config "$HOSTNAME"
		if ! which posInitBranchserver.sh &> /dev/null; then
			error "posInitBranchserver.sh is not installed."
			return $INT_ERROR_CODE;
		fi
		if [ $pos_version = 11 ]; then
			{
				# 1 = online, 2 = offline - only if admin server and branch server differs
				[ -z "$on_admin" ] && echo "1"
				echo "${organization}"
				echo "${country}"
				echo "${organizationalUnit}"
				echo "${scLocation}"
				echo "${LdapServer}"
				echo "${userPassword}"
				# run LDAP on localhost?
				echo "Y"
				if [ "$ssl"x = yx ]; then
					echo "Y"
				fi
				echo "${internal_ip}"
				# are you sure to do that?
				echo "Y"
			} | $COMMAND --reinitialize || { error "run_posInitBranchserver failed"; return $ERROR_CODE; }
		elif [ $pos_version = 10 ]; then
			{
				echo "${organization}"
				echo "${country}"
				echo "${LdapServer}"
				echo "cn=${admin},o=${organization},c=${country}"
				echo "${pass}"
				echo ""

			} | $COMMAND || { error "run_posInitBranchserver failed"; return $ERROR_CODE; }
		else
			workaround "Fixing incorect COUNTRY read"
			sed -i '83s/\[ -n $COUNTRY \] && COUNTRY="us"/[ -z "$COUNTRY" ] && COUNTRY="us"/' /usr/sbin/posInitBranchserver.sh
			{
				echo "${organization}"
				echo "${country}"
				echo "${LdapServer}"
				echo "cn=${admin},o=${organization},c=${country}"
				echo "${pass}"
				echo ""

			} | $COMMAND || { error "run_posInitBranchserver failed"; return $ERROR_CODE; }
		fi
	)

	do_base_check
}

fi # end of branch

########
# Non-LDAP stuff
########

fix_posReadPassword() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	##### this will replace implementation of '/usr/lib/SLEPOS/posReadPassword.pl' to something less aggressive to stdin #####
	case $pos_version in
		9|10)	POSREADPASSWORD=/usr/sbin/posReadPassword.pl ;;
		11)	POSREADPASSWORD=/usr/lib/SLEPOS/posReadPassword.pl ;;
	esac
	cat << EOB > "$POSREADPASSWORD" && chmod +x "$POSREADPASSWORD" || { error "An error occured during replacing /usr/lib/SLEPOS/posReadPassword.pl - slepos_lib.sh error"; return $INT_ERROR_CODE; }
#!/bin/sh
read pass
echo -n "\$pass"
EOB
}


show_log_on_fail() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

# Show logs of command only if it fails
#	$1	command to be run

	LOG="`$1 2>&1`"
	if [ $? -ne 0 ]; then
		error "---begin of error log"
		echo "$LOG"
		error "---end of error log"
		return $ERROR_CODE
	fi
}

if [ "$on_image" ]; then
# this function belongs to image server namespace only
put_image_to_admin_server() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	if [ "$1" = -f ]; then
		FORCE_UPDATE=-f
		shift
	else
		unset FORCE_UPDATE
	fi

	if [ "$on_admin" ]; then
		move_image $FORCE_UPDATE "$1"
	else
		tar cf - "$IMAGE_SOURCE_PATH/$1"/initrd-*netboot* "$IMAGE_SOURCE_PATH/$1/$1"* | \
		    ssh root@"$admin_server_name" "tar xf - -C / ; $SLEPOS_LIB_FILE move_image $FORCE_UPDATE '$1'" || \
		{ error "put_image_to_admin_server failed - probably slepos_lib.sh error"; return $ERROR_CODE; }
	fi
}
fi # on_image?


if [ "$on_admin" ]; then
# this function belongs to admin server namespace
move_image() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	This function moves image on admin server from the place where are located builds by kiwi, to the place where are expected
#	  for possyncimages.pl on branch server
#	if image server is not admin server, put_image_to_admin_server() will copy image to the same place onto admin server so
#	  this function is valid again

#	$1	image name

	if [ "$1" = -f ]; then
		FORCE_UPDATE=yes
		shift
	else
		unset FORCE_UPDATE
	fi

	# I need to separate NLPOS because of different hierarchy

	if [ "$pos_version" = 9 ]; then
		KERNEL="`ls "$IMAGE_SOURCE_PATH"/initrd-*netboot*kernel.* | head -n 1`" && \
		INITRD="`ls "$IMAGE_SOURCE_PATH"/initrd-*netboot*.gz | head -n 1`" && \
		mv "$IMAGE_SOURCE_PATH"/initrd-*netboot* "$BOOT_IMAGE_TARGET_PATH" && \
		mv "$IMAGE_SOURCE_PATH/$1"* "$SYSTEM_IMAGE_TARGET_PATH" || \
		{ error "move_image failed - is local_config.sh set correctly?"; return $ERROR_CODE; }
	else
		KERNEL="`ls "$IMAGE_SOURCE_PATH/$1"/initrd-*netboot*kernel.* | head -n 1`" && \
		INITRD="`ls "$IMAGE_SOURCE_PATH/$1"/initrd-*netboot*.gz | head -n 1`" && \
		mv "$IMAGE_SOURCE_PATH/$1"/initrd-netboot* "$BOOT_IMAGE_TARGET_PATH" && \
		mv "$IMAGE_SOURCE_PATH/$1/$1"* "$SYSTEM_IMAGE_TARGET_PATH" || \
		{ error "move_image failed - is local_config.sh set correctly?"; return $ERROR_CODE; }
	fi
	if [ "$FORCE_UPDATE" ] || { [ ! -f "$BOOT_IMAGE_TARGET_PATH/linux" ] && [ ! -f "$BOOT_IMAGE_TARGET_PATH/initrd.gz" ]; }; then
		# symlinks already exists, update only when forced
		info "Updating symlinks"
		rm -f "$BOOT_IMAGE_TARGET_PATH/linux" "$BOOT_IMAGE_TARGET_PATH/initrd.gz"
		ln -s "`basename $KERNEL`" "$BOOT_IMAGE_TARGET_PATH/linux" && \
		ln -s "`basename $INITRD`" "$BOOT_IMAGE_TARGET_PATH/initrd.gz"
	else
		warn "linux and initrd.gz symlinks already created - skipping"
	fi || \
	{ error "move_image failed - is local_config.sh set correctly?"; return $ERROR_CODE; }

}
fi # on_admin?

# these settings may be version dependant
# it is valid for SLEPOS 11
# TODO: SLEPOS 11 supports i586 image only
IMAGE_ARCH=i586

if [ "$on_image" ]; then

create_image() {
# create image using kiwi
#	$1	image template name (see $CONF_PATH/image-*.sh)
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	if [ -f "$CONF_PATH/image-$1.sh" ]; then
		info "Sourcing image-$1.sh and calling image preparations"
		(
			source "$CONF_PATH/image-$1.sh"
			# now I've got sourced this function and image configuration
			create_this_image "$1"
		)
	else
		info "No configuration found in $CONF_PATH - probably configuration created in YaST2 Image Creator"
	fi
}

check_copied_repo() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1	path to check
#	$2	path to ls-lR.gz file (optionable, but needed for SLES9)

	DEFAULT_DIR="${1%/}"
	LIST_FILE="${2="$DEFAULT_DIR/ls-lR.gz"}"
	LS_LR="`zcat "$LIST_FILE" | grep -v "^total"`"
	while read line; do
		if grep '^\..*:' <<< "$line" &>/dev/null; then
			DIR="${line%:}"
			DIR="${DIR#./}"
		elif grep '^[ld-]r' <<< "$line" &>/dev/null; then
			[ -f "$DEFAULT_DIR/$DIR/${line##* }" ] || \
			[ -d "$DEFAULT_DIR/$DIR/${line##* }" ] || \
			grep 'suse/src' <<< "$DIR" &> /dev/null || \
			echo "missing $DEFAULT_DIR/$DIR/${line##* }"
		fi
	done <<< "$LS_LR"
	unset LS_LR
}

find_iso_on_cml() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# find ISO on cml.suse.cz and return link
#	$1	version string (e.g. SLES-11-DVD-x86_64-GM-DVD1)
	wget "http://cml.suse.cz/cgi-bin/find-iso2?filter=$1" -o /dev/null -O - | sed -n "s@.*<a href='\([^\"]*${1}.iso\)'.*@\1@p"
}

get_iso_check_mount_copy_umount() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1	link to ISO file to be copied

	ISO_LINK="$1"
	ISO_NAME="`basename "$ISO_LINK"`"
	if [ -f "$ISO_ROOT/$ISO_NAME" ]; then
		info "previously downloaded $ISO_NAME found - skipping download"
	else
		info "getting $ISO_LINK"
		wget "$ISO_LINK" -O "$ISO_ROOT/$ISO_NAME" || { error "Cannot download $ISO_LINK"; return $INT_ERROR_CODE; }
	fi

	# if it is downloaded from cml.suse.cz, we can check SHA1 sums
	if grep 'cml.suse.cz' <<< $ISO_LINK &> /dev/null; then
		# check SHA1SUMS file located on cml.suse.cz
		info "checking SHA1 sums in file \"${ISO_LINK%%$ISO_NAME}SHA1SUMS\""
		SHA1SUMS="`wget -o /dev/null -O - "${ISO_LINK%%$ISO_NAME}SHA1SUMS"`" && \
		SHA1SUM="`sed -n "s@$ISO_NAME@$ISO_ROOT/$ISO_NAME@p" <<< "$SHA1SUM"`"
		if [ $? -eq 0 ]; then
			# we have found SHA1 sums for this file
			if sha1sum -c <<< "$SHA1SUM" &> /dev/null; then
				info "ISO SHA1 sums are correct"
			else
				error "ISO control sums failed! (SHA1SUM=$SHA1SUM)"
				return $INT_ERROR_CODE
			fi
		else
			warn "$ISO_NAME SHA1 sums weren't found, cannot check ISO file..."
		fi
	fi

	# now do the main job

	[ -d /root/loop ] || mkdir /root/loop
	umount /root/loop &> /dev/null

	info "Mounting $ISO_NAME" && \
	mount -o loop,ro "$ISO_ROOT/$ISO_NAME" /root/loop && \
	\
	info "Running poscdtool.pl (it will take a while)" && \
	poscdtool.pl --copy --source=/root/loop --type=cd && \
	info "Successfully done" && \
	\
	info "Unmounting $ISO_NAME" && \
	if grep /root/loop /etc/mtab &>/dev/null; then
		umount /root/loop &>/dev/null
	fi && \
	\
	if [ "$REMOVE_ISO" ]; then
		rm /root/"$ISO_NAME"
	fi && \
	info "$ISO_NAME was copied" || { error "An error occured"; return $INT_ERROR_CODE; }
}

# this function also belongs to image server namespace
copy_repositories() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

#	-r	remove ISO after download

# This will copy repositories to correct place by calling poscdtool.pl

# You can specify SLEPOS_ISO and SLES_ISO variables or just follow set SLEPOS_PATH/SLES_PATH once and change only version or
#   you can try to grep it from repository address (if you're installing from some remote repository...)

	if [ "$COPY_REPO" = done ]; then
		info "Already successfully passed (COPY_REPO=$COPY_REPO), skipping..."
		return 0
	fi

	if [ "$1" = -r ]; then
		REMOVE_ISO=-r
		shift
	else
		unset REMOVE_ISO
	fi

	if [ -z "$SLEPOS_ISO" ]; then

		# if we're on NLPOS9, we have to use list of ISO URLs, rest would be much more painful
		if [ "$pos_version" = 9 ]; then
			error "You need to specify SLEPOS_ISO array for NLPOS9"
			return $INT_ERROR_CODE
		fi

		ZYPPER_LR_OUT="`zypper lr -d | grep -v nu_novell_com`"
		info "Checking SLES 'string'..."
		if [ -z "$SLEPOS_STRING" ]; then
			SLEPOS_STRING="$(basename `cut -d\| -f8 <<<"$ZYPPER_LR_OUT" | grep -- -POS-`)"
		fi
		info "SLEPOS 'string' is $SLEPOS_STRING"


		# find this string on cml.suse.cz
		info "Looking for SLEPOS ISO image on cml.suse.cz..."
#		SLEPOS_ISO="$SLEPOS_PATH/`wget "$SLEPOS_PATH" -o /dev/null -O - | sed -n 's@.*<a href="\([^"]*\)">.*@\1@p' | grep "$SLEPOS_VERSION"`"
		SLEPOS_ISO=( "`find_iso_on_cml "$SLEPOS_STRING"`" )
		case "`wc -l <<< "$SLEPOS_ISO"`" in
			0)
				error "I wasn't able to find ISO, please, specify URL into SLEPOS_ISO"
				return $INT_ERROR_CODE;;
			1)
				info "$SLEPOS_ISO found" ;;
			*)
				if [ "`grep -v "UNTESTED" <<< "$SLEPOS_ISO" | wc -l`" = 1 ]; then
					SLEPOS_ISO="`grep -v "UNTESTED" <<< "$SLEPOS_ISO"`"
					info "$SLEPOS_ISO found"
				fi
		esac
	else
		info "SLEPOS ISO is set to ${SLEPOS_ISO[@]}"
	fi

	if [ -z "$SLES_ISO" ]; then

		# if we're on NLPOS9, we have to use list of ISO URLs, rest would be much more painful
		if [ "$pos_version" = 9 ]; then
			error "You need to specify SLES_ISO array for NLPOS9"
			return $INT_ERROR_CODE
		fi

		# SLES_STRING, for example 'SLES-11-DVD-x86_64-GM-DVD1'
		info "Checking SLES 'string'..."
		SLES_STRING="$(basename `cut -d\| -f8 <<<"$ZYPPER_LR_OUT" | grep SLES | sed 's/x86_64/i586/'`)"
		info "SLES 'string' is $SLES_STRING"

		# find this string on cml.suse.cz
		info "Looking for SLES ISO image on cml.suse.cz..."
		SLES_ISO=( "`find_iso_on_cml "$SLES_STRING"`" )
	else
		if echo "$SLES_ISO$" | grep '@' >/dev/null; then
			info "SLES ISO is set to:"
			for a in $(echo "$SLES_ISO" | sed 's/[^@]*\(@.*@\)[^@]*/\1/' | tr '@' ' '); do
				echo "$SLES_ISO" | sed "s/\([^@]*\)@.*@\([^@]*\)/\1$a\2/"
				#need to do something with it !!!!!!!
			done
		else
			info "SLES ISO is set to ${SLES_ISO[@]}"
		fi
	fi

	umount /root/loop &> /dev/null

	for ISO in "${SLEPOS_ISO[@]}" "${SLES_ISO[@]}"; do
		get_iso_check_mount_copy_umount $REMOVE_ISO "$ISO" || { error "Cannot download/mount/copy/umount $ISO image..."; return $ERROR_CODE; }
	done
}

fi # on_image?


run_posleases2ldap_oneshot(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	# runs in debug mode in local console
	if [ -e /var/run/posleases2ldap.pid ] && ps aux | grep "^[^[:blank:]]\+[[:blank:]]\+`cat /var/run/posleases2ldap.pid `" | \
		grep /usr/sbin/posleases2ldap.pl &> /dev/null; then
			echo "posleases2ldap is already running"
			return $ERROR_CODE
	else
		#/usr/sbin/posleases2ldap.pl -v debug -o
		#pro 11 sp 1
		if [ "$pos_version" = 11 -a "$pos_patchlevel" = 1 ]; then
			/usr/sbin/posleases2ldap.pl -v debug -o
		else
			/usr/sbin/posleases2ldap.pl -d -v -o
		fi
		do_base_check "$?"
        fi
}

restart_posleases2ldap(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	#kill it, if that's needed
	if [ -e /var/run/posleases2ldap.pid ] && ps aux | grep "^[^[:blank:]]\+[[:blank:]]\+`cat /var/run/posleases2ldap.pid `" | \
		grep /usr/sbin/posleases2ldap.pl &> /dev/null; then
		killall posleases2ldap.pl;

	fi
	#and start
	/usr/sbin/posleases2ldap.pl
	do_base_check "$?"

}

transfer_config() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# parameters
#	$1	computer name

	tar cf - "$CONF_PATH"/* "$SLEPOS_LIB_FILE" "$LOCAL_CONFIG" | ssh -o StrictHostKeyChecking=no "root@$1" "tar xf - -C /"
	do_base_check
}

bender_backup() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# parameters
#	$1	computer name

	tar cf - "$CONF_PATH"/* "$SLEPOS_LIB_FILE" "$LOCAL_CONFIG" | ssh "root@bender" "cat > qa_slepos.tar"
}

if [ -n "$on_admin" ]; then

workaround_507842() {
	if [ "$ssl"x = nx ]; then
		if [ "$pos_version" != 9 ]; then
			workaround "Bug 507842 - removing certificates"
			[ -f "/srv/SLEPOS/certs/ca.crt" ] && rm /srv/SLEPOS/certs/ca.crt || true
		fi
	fi
}

workaround_506161() {
	# FIXME: Workaround for bnc#506161 and maybe later
 	workaround "bug 506161 - removing cn=minimal,cn=default,cn=global,o=${organization},c=${country}"
 	posAdmin.pl \
 		--user "cn=${admin},o=${organization},c=${country}" \
 		--password "${pass}" \
 		--remove \
 		--DN "cn=minimal,cn=default,cn=global,o=${organization},c=${country}" \
 		--recursive
}

do_admin() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# Cumulative function for admin server

	workaround_507842
	firewall_ports admin_server_ports

	run_posInitLdap && \
	workaround_506161
	create_database
	info "Checking for already built images..."
	if [ "$pos_version" = "9" ]; then
		#wtf, there are absolutelly differrent naming for images
		BUILT_IMAGES_TO_ADD="`find "$SYSTEM_IMAGE_TARGET_PATH" -type f | sed "s@${SYSTEM_IMAGE_TARGET_PATH}/@@" | grep -v '\.md5$' | sed 's@-[^-]*-[^-]*-[^-]*-[^-]*$@@' | sort -u`"
	else
		BUILT_IMAGES_TO_ADD="`find "$SYSTEM_IMAGE_TARGET_PATH" -type f | sed "s@${SYSTEM_IMAGE_TARGET_PATH}/@@" | grep -v '\.md5$' | sed 's@-[^-]*$@@' | sed 's@\.\(i[56]86\|x86_64\)@@' | sort -u`"
	fi
	if [ "$BUILT_IMAGES_TO_ADD" ]; then
		info "Already built images found, adding to LDAP..."
		for IMAGE in $BUILT_IMAGES_TO_ADD; do
			show_log_on_fail "add_image_to_ldap $IMAGE" || { error "add_image_to_ldap failed on $IMAGE"; return $ERROR_CODE; }
		done
	fi
}

create_scPxeFileTemplate() {
	# $baseDN should look like cn=machine,cn=global,o=${organization},c=${country}
	posAdmin.pl \
		--user "cn=${admin},o=${organization},c=${country}" \
		--password "${pass}" \
		--base "${baseDN}" \
		--add \
			--scPxeFileTemplate \
			--cn "${scPxeFileTemplate}" \
			--scMust "${scMust}" \
			--scKernelParameters "${scKernelParameters}"
}

add_kernel_parameters() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1	DN of affected scCashRegister object
#	$2	kernel parameters to be added
#	$3	must use these parameters [TRUE|FALSE] (false means may)
#	$4	name of scPxeFileTemplate

	(
		case $# in
			4) scPxeFileTemplate="$4"; scMust="${3}" ;;
			3) scPxeFileTemplate="default"; scMust="${3}";;
			*) scPxeFileTemplate="default"; scMust="TRUE";;
		esac

		scKernelParameters="$2"
		baseDN="$1"
		show_log_on_fail "create_scPxeFileTemplate" || { error "add_kernel_parameters failed ($@)"; return $ERROR_CODE; }
	)
}

fi #on admin

if [ -z "$on_branch" ]; then
# I'm not on branch server - run do_branch on remote machine
do_branch() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	if [ -z "$1" ]; then
		echo "Sorry, you're not on branch server, so you need to specify branch server as parameter."
		echo "Usage:"
		echo "    do_branch <branch_server_name>"
		echo
		return $INT_ERROR_CODE
	else
		transfer_config_to_branch "$1"
		ssh root@"$1" "$SLEPOS_LIB_FILE do_branch"
	fi
}

do_all_branch() {
	for i in "$branch_server_list"; do
		info "Transfering config"
		transfer_config "$i"
		info "Running do_branch on $i"
		do_branch "$i"
	done
}

else
# I'm on branch server - do the job
branch_net_up() {
	info "Bringing internal network up"
	(
		read_branch_server_config "$HOSTNAME"
		ifconfig "$device" "$internal_ip" up
		[ "$pos_version" -ne 9 ] && yast2 firewall interfaces add "interface=$device" zone=INT
	)
}

do_branch() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# Cumulative function for branch server
# No parameters
	branch_net_up
	# enable ports on firewall (check local_config.sh), not working on NLPOS 9
	firewall_ports branch_server_ports

	info "Running posInitBranchserver.sh"
	run_posInitBranchserver && \
	info "Syncing images from Admin server" && \
	possyncimages.pl && \
	info "Starting posleases2ldap service" && \
	rcposleases2ldap start
}

fi # on_branch?

do_image() {
# Cumulative function for image server
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	copy_repositories
	# for every image configuration file
	for i in "$CONF_PATH"/image-*.sh; do
		IMAGE_NAME="${i##$CONF_PATH/image-}"
		IMAGE_NAME="${IMAGE_NAME%%.sh}"
		# create image, copy to the right place and create scPosimage objects in LDAP
		create_image "$IMAGE_NAME" && \
		put_image_to_admin_server -f "$IMAGE_NAME" && \
		add_image_to_ldap "$IMAGE_NAME"
	done
}

check_admin() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# This function tests status after run_posInitLdap
	rcldap status &> /dev/null || error "LDAP is not running!"
}

check_branch() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
# This function tests status after run_posInitBranchserver
	rcdhcpd status &> /dev/null || error "DHCP is not running!"
	rcatftpd status &> /dev/null || error "aTFTP is not running!"
	rcnamed status &> /dev/null || error "aTFTP is not running!"
	rcposleases2ldap status &> /dev/null || error "POSleases2LDAP is not running!"
}

ls_images() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	if [ "$on_admin" ]; then
		info "Images on admin server:"
		ls "${SYSTEM_IMAGE_TARGET_PATH%/}"
	fi      
	if [ "$on_branch" ]; then
		info "Images on branch server:"
		ls "${BRANCH_IMAGE_PATH%/}"
	fi      
	if [ "$on_image" ]; then
		info "Images on image server:"
		ls "${IMAGE_SOURCE_PATH%/}"
	fi      
	if [ -z "$on_admin" ] && [ -z "$on_branch" ] && [ -z "$on_image" ]; then
		error "Sorry - I don't know where to search for images..."
		# so far only interactively called
		return $INT_ERROR_CODE
	fi
}

check_config() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	echo "Admin server name:        $admin_server_name"
	echo "Admin server IP:          $admin_server_IP"
	admin_server_read_IP="`host "$admin_server_name" | cut -d\  -f4`"
	if [ "$admin_server_IP" != "$admin_server_read_IP" ]; then
		error "IP address of admin server differs (admin_server_IP = $admin_server_IP, but IP address found is "$admin_server_read_IP")"
	fi
	echo "Branch servers:"
	for i in "$CONF_PATH"/branch_server-*.sh; do
		NAME="${i##${CONF_PATH}/branch_server-}"
		NAME="${NAME%.sh}"
		echo "	$NAME"
	done
	echo
	echo -n "SSL for LDAP is "
	if [ "$ssl"x = yx ]; then
		echo "enabled"
	else
		echo "disabled"
	fi
}

#FIXME: part of check_deps.sh?
all_exe_files() {
	echo $PATH | \
	tr ':' '\n' | \
	while read dir; do
		[ -d "$dir" ] && \
		[ $(ls -1A "$dir" | wc -l) -gt 0 ] && \
		echo "$dir"
	done | \
	sed 's@$@/*@'
}

atftp_test() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }

	(
		MY_HOSTNAME="${1:-$HOSTNAME}"
		source "${CONF_PATH}/branch_server-${MY_HOSTNAME}.sh"
		atftp -g -l /dev/stdout -r boot/pxelinux.cfg/default "$internal_ip"
	)
}

configure_external_dhcp() {
	ssh -t root@"$ExtDHCP_machine" \
"yast2 dhcp-server interface select=\"$ExtDHCP_interface\" && \
yast2 dhcp-server subnet min-ip=\"$ExtDHCP_range_min\" && \
yast2 dhcp-server subnet max-ip=\"$ExtDHCP_range_max\" && \
yast2 dhcp-server subnet default-lease-time=\"$ExtDHCP_default_time\" && \
yast2 dhcp-server subnet max-lease-time=\"$ExtDHCP_max_time\" && \
yast2 dhcp-server enable
yast2 dhcp-server options set key=domain-name value=\"$scLocation.$organizationalUnit.$organization.$country\"
"
${},ou=
}

if [ -z "$on_branch" ]; then
# NOTE: on admin server ssh into BS
#FIXME: this function is redundant, but more advanced than check_branch, remove/rename it
check_BS_state() {
#	$1 BS name
	ssh root@"$1" "$SLEPOS_LIB_FILE check_BS_state"
}
else # on_branch
# NOTE: on BS call directly
check_BS_state() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	
	#dhcpcd_line="$(ps auwwxf | grep dhcpcd | grep -v grep)"
	#root     27860  0.0  0.0   8148   540 ?        Ss   Mar11   0:00 /sbin/dhcpcd --netconfig -L -E -HHH -c /etc/sysconfig/network/scripts/dhcpcd-hook -t 0 -h linux-3bna eth0
	
	x="$(
	ps auwwx | grep dhcpcd | grep -v grep | while read user pid x1 x2 x3 x4 x5 state startdate timerun command; do
		#(( cycle_run += 1 ));
		#echo "###c $cycle_run"
		if [ "$command" == "/sbin/dhcpcd --netconfig -L -E -HHH -c /etc/sysconfig/network/scripts/dhcpcd-hook -t 0 -h linux-3bna eth0" ]; then
			#modify it by proper eth
			#(( dhcpcd_state += 1 ));
			#echo "###d $dhcpcd_state"
			echo -n "d"
		fi
		echo "c"
		#export cycle_run
		#export dhcpcd_state
	done
	)"

	cycle_run="$(wc -l <<< "$x")"
	dhcpcd_state="$(echo "$x" | grep 'd' | wc -l)"

	if [ "$cycle_run" == '0' ]; then
		error "No dhcpcd running"
	elif [ "$cycle_run" -gt '1' ]; then
		error "Too much dhcpcd running"
	fi
	if [ "$dhcpcd_state" != '1' ]; then
		error "Probably not properly configured dhcpcd"
	fi	

	resolv_conf_line="$(grep -v '^#' /etc/resolv.conf)"
	# search GrandKanal.vinohrady.PrazskeKanalizace.pl suse.cz suse.de
	if ! grep "^search $scLocation.$organizationalUnit.$organization.$country suse.cz suse.de\$" &> /dev/null <<< "$resolv_conf_line" ; then
		error "Unproperly configured /etc/resolv.conf"
	fi

	ping -c 4 tftp > /dev/null
	tftp_ping="$?"	
	if [ "$tftp_ping" != '0' ]; then
		error "Can't ping tftp."
	fi

	local POSL_PROCESS_COUNT="$(ps aux | grep 'posleases2ldap.pl' | grep -v grep | wc -l )" 
	if [ "$POSL_PROCESS_COUNT" -ne '2' ] ; then
		error "There should be two posleases2ldap.pl running processes; There is/are $POSL_PROCESS_COUNT of them."
	fi

	# do check if that's O.K.
	info "BS check done."
	return 0
}

fi # on_branch


find_interface_by_mac() {
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
	unset remote
	if [ "$#" -eq 2 ]; then
		remote="$1"
		shift
	fi
	ADDRESS="`tr [A-Z] [a-z] <<< "$1"`"
	if [ "$remote" ]; then
		ssh root@"$remote" \
		"for i in /sys/class/net/*; do
			if [ \"$ADDRESS\" = \"`cat \$i/address`\" ]; then
				echo \"\${i##/sys/class/net/}\"
				break
			fi
		done"
	else
		for i in /sys/class/net/*; do
			if [ "$ADDRESS" = "`cat $i/address`" ]; then
				echo "${i##/sys/class/net/}"
				break
			fi
		done
	fi
}

find_the_other_interface() {
	ssh root@"$1" 'DEFAULT_ROUTE="`sed -n "s@^\([0-9a-z]*\)[[:blank:]]\+00000000.*@\1@p" /proc/net/route`"
		THE_OTHER="`ls /sys/class/net/ | grep -v "^lo$" | grep -v "^$DEFAULT_ROUTE$"`"
		if [ "`wc -l <<< "$THE_OTHER"`" -eq 1 ]; then
			echo "$THE_OTHER"
		fi
		'
}

get_value(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1 file name
#	$2 variable name
#
# it returns variable value to stdout

	tmp="$(grep "$2=" "$1" | grep -v '^#' | sed 's/^[ \t]*//' | tail -n 1)"
	if grep "^$2='" >/dev/null <<< "$tmp"; then
		out="$(sed "s/$2='\([^']*\)'.*/\1/" <<< "$tmp")"
	else
		if grep "^$2=\"" &>/dev/null <<< "$tmp"; then
			out="$(sed "s/$2="\"\([^\"]*\)".*/\1/" <<< "$tmp")"
		else
			out="$(sed "s/$2=\([^ ]*\) .*/\1/p" <<< "$tmp")"
		fi
	fi
	echo "$out"
}

is_variable(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1 file name
#	$2 variable name
#
# it returns 0 (means variable is in the file) or 2 (means it isn't)

	tmp="$(grep "$2=" "$1" | sed 's/^[ \t]*//' | grep -v '^#')"
	if grep "^$2=" >/dev/null <<< "$tmp"; then
		return $SUCCESS_CODE;
	else
		return $INT_ERROR_CODE;
	fi
}

put_variable(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1 file name
#	$2 variable name
#	$3 variable value

	echo "$2='$3'" >> "$1"
}

get_MAC(){
	is_help_requested "$@" && { handle_help "$FUNCNAME" ; return $SUCCESS_CODE ; }
#	$1 devicename (eth0, eth1 ...)
	cat /sys/class/net/"$1"/address 2> /dev/null || return "$INT_ERROR_CODE"
}

mk_sysconfig_eth(){
#	$1 devicename (eth0, eth1 ...)
#	$2 IP (Mask is 24bit)

	netfile="/etc/sysconfig/network/ifcfg-$1"
	tmpnetfile="/tmp/slepos_lib_tmp_netfile"

	mac="$(get_MAC "$1")"
	
	if [ -z "$mac" ]; then
		return $INT_ERROR_CODE;
	fi

	broadcast="`sed 's/\.[^.]*$/.255/' <<< "$2" `"

	echo -n > "$tmpnetfile"
	put_variable "$tmpnetfile" BOOTPROTO auto
	put_variable "$tmpnetfile" IPADDR "$2"
	put_variable "$tmpnetfile" BROADCAST "$broadcast"
	put_variable "$tmpnetfile" LLADDR "$mac"
	put_variable "$tmpnetfile" STARTMODE onboot
	put_variable "$tmpnetfile" NAME 'SLEPOS internal network'
	
	if [ -e "$netfile" ]; then
		# is old data correct?
		# test BOOTPROTO na dhcp!!!
		
		file_status=yes

		if is_variable "$netfile" BOOTPROTO; then
			if [ "$(get_value "$netfile" BOOTPROTO)" = dhcp ]; then
				file_status=no
				warn "The interface was configured by DHCP. That isn't seemt to be proper interface for internal SLEPOS network"
			fi
			if [ "$(get_value "$netfile" BOOTPROTO)" = dhcp4 ]; then
				file_status=no
				warn "The interface was configured by DHCP. That isn't seemt to be proper interface for internal SLEPOS network"
			fi
			if [ "$(get_value "$netfile" BOOTPROTO)" = "dhcp+autoip" ]; then
				file_status=no
				warn "The interface was configured by DHCP. That isn't seemt to be proper interface for internal SLEPOS network"
			fi
		fi
		if is_variable "$netfile" IPADDR; then
			if ! get_value "$netfile" IPADDR | grep '^192.168.' &> /dev/null ; then
				file_status=no
				warn "The interface's IP wasn't from 192.168.x.x range. That isn't seems to be proper interface for internal SLEPOS network"
			fi
		fi
		if [ "$file_status" = no ]; then
			warn "If you're sure, that you want to use interface $1 as internal SLEPOS interface, remove the $netfile file please"
			return $INT_ERROR_CODE
		fi

		if diff "$tmpnetfile" "$netfile" &> /dev/null; then
			info "The generated $netfile file is the same as previous."
		else
			cp "$netfile" /root/slepos_lib_sysconfig_network_backup
			info "$netfile has been backuped into /root/slepos_lib_sysconfig_network_backup and overwritten by new configuration."
			mv "$tmpnetfile" "$netfile"
		fi
	else
		mv "$tmpnetfile" "$netfile"
	fi
}

show_help() {
cat << EOB
SLEPOS command library v$VERSION
Using configuration located in $CONF_PATH

commands available:
    run_posInitLdap
    run_posInitBranchserver
    create_database
    ldap_search
    ldap_search_branch
    copy_repositories
    do_base_check
    assign_image_to_workstation
    set_default_image
    change_image_version
    change_image_file
    add_image_to_ldap
    del_image_from_ldap
    add_image_to_ldap_in_container
    add_container_to_ldap
    put_image_to_admin_server
    move_image
    create_image
    check_copied_repo
    transfer_config
    bender_backup
    ls_images
    check_admin
    check_branch
    check_config
    atftp_test
    configure_external_dhcp
    check_BS_state
    show_help

additional commands (but not supposed to be called directly):
    info
    error
    error_internal
    warn
    workaround
    firewall_ports
    unwrap_ldap
    create_scServerContainer
    create_scBranchserver
    create_scLocation
    create_scNetworkcard
    create_scPosimage
    remove_scPosimage
    create_scPosimage_in_container
    create_scDistributionContainer
    create_scCashRegister
    create_scRamDisk
    create_scHarddisk
    create_tftp_service
    create_dhcp_service
    create_dns_service
    create_OU
    create_scWorksctation
    modify_scWorkstation
    modify_scCashRegister
    modify_scPosImage
    remove_cr_conf
    fix_posReadPassword
    show_log_on_fail
    get_iso_check_mount_copy_umount
    workaround_507842
    workaround_506161
    create_scPxeFileTemplate
    add_kernel_parameters
    branch_net_up
    find_interface_by_mac
    find_the_other_interface
    is_help_requested
    handle_help
    all_exe_files

server type based cumulative commands:
    do_admin
    do_branch
    do_all_branch
    do_image
EOB
}

is_help_requested() {
	unset HELP LIST
	for i in "$@"; do
		if [ "$i" = "-h" ] || [ "$i" = "--help" ]; then
			HELP=yes
		elif [ "$i" = "-l" ] || [ "$i" = "--list" ]; then
			LIST=yes
		fi
	done
	[ "${HELP}${LIST}" ]
}

handle_help() {
	case "$1" in
		"run_posInitLdap")
			echo "run_posInitLdap"
			echo "automated run of posInitLdap.sh using configuration from $CONF_PATH"
			echo "usage:"
			echo "    run_posInitLdap" ;;
		"run_posInitBranchserver")
			echo "run_posInitBranchserver"
			echo "automated run of posInitBranchserver.sh using configuration from $CONF_PATH"
			echo "usage:"
			echo "    run_posInitBranchserver" ;;
		"create_database")
			echo "create_database"
			echo "automated creation of object in LDAP database using configuration from $CONF_PATH"
			echo "usage:"
			echo "    create_database" ;;
		"ldap_search")
			echo "ldap_search"
			echo "ldapsearch query of admin server"
			echo "usage:"
			echo "	ldap_search <query> [base]" ;;
		"ldap_search_branch")
			echo "ldap_search_branch"
			echo "ldapsearch query of branch server"
			echo "usage:"
			echo "	ldap_search_branch <query> [base]" ;;
		"copy_repositories")
			echo "copy_repositories"
			echo "automated copy of repositories using poscdtool.pl"
			echo "It respects these variables:"
			echo "    ISO_ROOT - download location for ISOs"
			echo "    COPY_REPO - when set to done, copy_repositories just exits"
			echo "    LINK_REPO - link repository from ISO file instead of copying its contents"
			echo "usage:"
			echo "    copy_repositories" ;;
		"do_admin")
			echo "do_admin"
			echo "metacommand for running all available tests and commands on admin server"
			echo "currently is consists of:"
			echo "    workaround_507842"
			echo "    firewall_ports"
			echo "    run_posInitLdap"
			echo "    workaround_506161"
			echo "    create_database"
			echo " 	  add already built images to newly created LDAP"
			echo
			echo "usage:"
			echo "    do_admin" ;;
		"do_branch")
			echo "do_branch"
			echo "metacommand for running all available tests and commands on branch server"
			echo "IMPORTANT NOTE: This function is on both admin server and branch server, so you can call"
			echo "it remotely"
			echo "Usage on branch server:"
			echo "    do_branch"
			echo "Usage on other machine:"
			echo "    do_branch <branch_server_name>"
			echo
			if [ "$on_branch" ]; then
				echo "You're currently on branch server."
			else
				echo "You are not on branch server now."
			fi
			echo
			echo "currently is consists of:"
			echo "    branch_net_up"
			echo "    firewall_ports"
			echo "    run_posInitBranchserver"
			echo "    possyncimages.pl (not a function - it's SLEPOS command)"
			echo "    rcposleases2ldap start" ;;
		"do_all_branch")
			echo "Remotelly calls do_branch() each branch server defined in \$branch_server_list (currently set to '$branch_server_list'). For more info look at do_branch"
			echo "usage:"
			echo "    do_all_branch" ;;
		"do_image")
			echo "do_image"
			echo "metacommand for running all available tests and commands on 'image server'"
			echo "currently is consists of:"
			echo "    copy_repositories"
			echo "    for every IMAGE defined in $CONF_PATH do:"
			echo "        create_image IMAGE"
			echo "        put_image_to_admin_server IMAGE"
			echo "        add_image_to_ldap IMAGE" ;;
		"add_image_to_ldap")
			echo "add_image_to_ldap"
			echo "create scPosimage object in LDAP"
			echo "this is useful for images you built"
			echo "usage:"
			echo "    add_image_to_ldap <image_name>" ;;
		"add_image_to_ldap_in_container")
			echo "add_image_to_ldap_in_container"
			echo "create scPosimage object in LDAP in specified container"
			echo "this is useful for images you built"
			echo "usage:"
			echo "    add_image_to_ldap <image_name> <container_name>" ;;
		"assign_image_to_workstation")
			echo "assign_image_to_workstation"
			echo "This will allow you to change image assigned to scWorkstation object"
			echo "usage:"
			echo "    assign_image_to_workstation <DN_of_the_scWorkstation> <scPosImageDn> [scPosImageVersion]"
			echo "example:"
			echo "    assign_image_to_workstation cn=CR01,cn=GrandKanal,ou=vinohrady,o=PrazskeKanalizace,c=pl cn=minimal,cn=default,cn=global,o=PrazskeKanalizace,c=pl \"3.1.3;active\"";;
		"add_container_to_ldap")
			echo "This will add scDistributionContainer to LDAP - needed for more kernels on one time"
			echo "usage:"
			echo "    add_container_to_ldap <container_name> <kernel_name> <kernel_version> <initrd_name>";;
		"show_help")
			echo "This will show generic help." ;;
		"set_default_image")
			echo "Sets default image, which will be set when no other matchs"
			echo "usage:"
			echo "    set_default_image <image_name>" ;;
		"change_image_version")
			echo "Changes version attribute of image in LDAP."
			echo "usage:"
			echo "    change_image_version <image_name> <version_string>" ;;
		"change_image_file")
			echo "Changes image file attribude in LDAP."
			echo "usage:"
			echo "    change_image_file <image_name> <filename>" ;;
		"del_image_from_ldap")
			echo "Removes image entry from LDAP"
			echo "usage:"
			echo "    del_image_from_ldap <image_name>" ;;
		"put_image_to_admin_server")
			echo "This function moves image from image server to admin server. When image server is the same machine as admin server, move_image is called."
			echo "usage:"
			echo "    put_image_to_admin_server [-f] <image_name>"
			echo
			echo "    -f        force update symlinks for kernel and initrd" ;;
		"move_image")
			echo "This function moves image from the place where image build tools created to the place where admin server expect that."
			echo "usage:"
			echo "    move_image [-f] <image_name>"
			echo
			echo "    -f        force update symlinks for kernel and initrd" ;;
		"create_image")
			echo "Build image according to $CONF_PATH/image-IMAGE.sh"
			echo "usage:"
			echo "    create_image <IMAGE>" ;;
		"check_copied_repo")
			echo "Checks if all files in repository were copied. For the check there is used ls-lR.gz file."
			echo "usage:"
			echo "    check_copied_repo <copied_repository_path>" ;;
		"transfer_config")
			echo "Copy configuration and slepos_lib.sh to another computer."
			echo "usage:"
			echo "    transfer_config <hostname>" ;;
		"bender_backup")
			echo "This function is for backing up current development state to bender.suse.cz, not much useful for other use."
			echo "usage:"
			echo "    bender_backup" ;;
		"ls_images")
			echo "List files in image path (different for admin server, branch server or image server."
			echo "usage:"
			echo "    bender_backup" ;;
		"check_admin")
			echo "Trivial check of admin server status."
			echo "usage:"
			echo "    check_admin" ;;
		"check_branch")
			echo "Trivial check of branch server status. Try to use check_BS_state() instead."
			echo "usage:"
			echo "    check_branch" ;;
		"check_config")
			echo "Shows some configuration informations"
			echo "usage:"
			echo "    check_config" ;;
		"atftp_test")
			echo "Simple test if atftp is running on proper network interface."
			echo "usage:"
			echo "    atftp_test <hostname>" ;;
		"configure_external_dhcp")
			echo "Remote setup of external DHCP server by calling \`yast2 dhcp-server'. You have to have set ExtDHCP_* variables."
			echo "usage:"
			echo "    configure_external_dhcp" ;;
		"check_BS_state")
			echo "More advanced check of branch server status."
			echo "usage:"
			echo "    check_BS_state" ;;
		*)
			echo "Sorry, not available. It means not implemented yet or you're not supposed to call it directly."
			echo "use show_help() to see global help" ;;
	esac
}

if [ -z "$is_sourced" ] && [ "$*" ]; then
	if is_help_requested "$1"; then
		show_help
	else
		"$@"
	fi
fi



