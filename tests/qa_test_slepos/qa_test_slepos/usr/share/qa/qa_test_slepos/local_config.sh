#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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

######
# Admin server configuration
# rest of configuration (located in the other files) is not machine dependant
#
# if you want to use other branch server, rename some already existing
# branch_server-hostname.sh to your desired name. Configuration is copied to
# branchserver on calling:
#
#	transfer_config <your_branchserver_name>
#
#######

################################################################################
############################ This is a MUST ####################################
################################################################################
#                                                                              #
# admin server configuration                                                   #
# NOTE: for NLPOS9 you have to put fully qualified name                        #
admin_server_name="foo"                                                        #
#                                                                              #
# names of branch servers to be used (space separated)                         #
# never use fully qualified name                                               #
# if not set, all defined branch servers will be set up in LDAP                #
branch_server_list="bar1 bar2 bar.domain.com"                                  #
#                                                                              #
# image server name - needed when admin server and image server are two        #
# different machines and you want to run all from the ctcs2 automation suite   #
# image_server_name="foo2"                                                     #
#                                                                              #
# you can specify internal network interface for each branch server            #
# it will have precedence over device                                          #
# in $CONF_PATH/branchserver-citharischius.sh                                  #
# bar1_internal_device=eth0                                                    #
#                                                                              #
# you can also specify MAC address of branch server here                       #
# bar2_internal_mac=00:11:22:33:44:55                                          #
#                                                                              #
# NOTE: use underscore instead of dash for these variables                     #
#                                                                              #
#                                                                              #
# You have to also unset or change this to confirm that values were altered    #
CONFIG_EDITED=no
################################################################################
################################################################################

# use SSL for LDAP? (y/n)
ssl=n

#get admin_server_IP
admin_server_IP="`host "$admin_server_name" | cut -d\  -f4`"

# location, where all not assigned branchserver will belong to
location_default=1

# default IP address for internal network interface
default_internal_ip="192.168.123.1"

# This firewall settings works for SLEPOS 10 or 11, you have to do it by hand for NLPOS9
# ports to open on admin server firewall - LDAP, LDAPS, rsync
admin_server_ports="389 636 873"

# ports to open on branch server firewall - tftp
branch_server_ports="69"

######
# This configuration will be used for image server
# for building images you need to copy repositories
# ISO are used for that
#######

# where downloaded ISO will be stored
# change it to some NFS if you're reinstalling SLEPOS frequently
ISO_ROOT="/root"

# if you have prepared medias in /var/lib/SLEPOS/dist or /opt/SLES/POS/dist
# uncomment this one:
# COPY_REPO=done

# if you prefer linking SLEPOS medias instead of copying, uncomment this
# LINK_REPO=y

# for easy adding of updated repository use this variable
# (it's used in template_image.sh)
# IMAGE_UPDATES="--add-repo http://sphinx/repo/\$RCE/SLES11-Updates/sle-11-i586/ 
#  --add-repotype rpm-md --add-repoprio 10 
#  --add-repo http://sphinx/repo/\$RCE/SLE11-POS-Updates/sle-11-i586 
#  --add-repotype rpm-md --add-repoprio 20"


# architecture of images to be downloaded
pos_version="`sed -n '/VERSION/s/[^=]*= //p' /etc/slepos-release`"
# get patchlevel 0, 1 ...
if [ -f /etc/slepos-release ]; then
	pos_patchlevel="`sed -n '/PATCHLEVEL/s/[^=]*= //p' /etc/slepos-release`"
else
	pos_patchlevel="`cat /etc/SuSE-release | sed -n 's/PATCHLEVEL = //p'`"
fi
case "$pos_version" in
	11)
		# when not yet released, this can get specified version automatically
		#SLEPOS_VERSION="RC1"

		if [ "$pos_patchlevel" -eq '0' ]; then		
			# if you specify SLES_ISO and SLEPOS_ISO, SLEPOS_VERSION will be ignored
			# SLES_ISO is array because of multiple installation sources needed in NLPOS9
			SLES_ISO=( "ftp://cml.suse.cz/install/iso/SLE11/SLES11-GM/SLES-11-DVD-i586-GM-DVD1.iso" )
			SLEPOS_ISO=( "ftp://cml.suse.cz/sync/SLE-11-POS-GM/SLE-11-POS-i586-x86_64-GM-Media.iso" )
		fi
		if [ "$pos_patchlevel" -eq '1' ]; then		
			# if you specify SLES_ISO and SLEPOS_ISO, SLEPOS_VERSION will be ignored
			# SLES_ISO is array because of multiple installation sources needed in NLPOS9
			SLES_ISO=( "http://fallback.suse.cz/install/SLES-11-SP1-GMC3/SLES-11-SP1-DVD-i586-GMC3-DVD1.iso" )
			SLEPOS_ISO=( "http://fallback.suse.cz/install/SLE-11-SP1-POS-GM/SLE-11-SP1-POS-CD-i586-x86_64-GM-DVD.iso" )
		fi

		# where are located SLEPOS templates for kiwi image building
		SLEPOS_TEMPLATE_PATH="/usr/share/kiwi/image/SLEPOS"

		# path, where are located image definitions and chroots right before building
		IMAGE_PATH="/var/lib/SLEPOS/system"

		# where are located finished images after its creation?
		IMAGE_SOURCE_PATH="$IMAGE_PATH/images"

		# where should boot images be located on admin server to be distributed to branch servers?
		BOOT_IMAGE_TARGET_PATH="/srv/SLEPOS/boot"

		# where should system images be located on admin server to be distributed to branch servers?
		SYSTEM_IMAGE_TARGET_PATH="/srv/SLEPOS/image"

		# where should system images be located on image server?
		BRANCH_IMAGE_PATH="/srv/tftpboot/image/"
		;;
	10)
		# you probably don't need to change these URLs since it is already released
		SLEPOS_ISO="ftp://cml.suse.cz/sync/SLES-10-SLEPOS/SLES-10-SLEPOS-10-GM-CD1.iso"
		SLES_ISO=(
			"ftp://cml.suse.cz/install/iso/SLE10/SLES-10-SP1-GM/SLES-10-SP1-DVD-i386-GM-DVD1.iso"
			"ftp://cml.suse.cz/install/iso/SLE10/SLED-10-SP1-GM/SLED-10-SP1-DVD-i386-GM-DVD1.iso"
		)
		
		# where are located SLEPOS templates for kiwi image building
		SLEPOS_TEMPLATE_PATH="/usr/share/kiwi/image/SLEPOS"

		# path, where are located image definitions and chroots right before building
		IMAGE_PATH="/var/lib/SLEPOS/system"

		# where are located finished images after its creation?
		IMAGE_SOURCE_PATH="$IMAGE_PATH/images"

		# where should boot images be located on admin server to be distributed to branch servers?
		BOOT_IMAGE_TARGET_PATH="/srv/SLEPOS/boot"

		# where should system images be located on admin server to be distributed to branch servers?
		SYSTEM_IMAGE_TARGET_PATH="/srv/SLEPOS/image"

		# where should system images be located on image server?
		BRANCH_IMAGE_PATH="/srv/tftpboot/image/"

		;; # end of SLEPOS 10/11 definitions

	9)
#			Needed media can be found here:
#			This links are usable with bugzilla account.
#			wget --http-user=bugzilla_name --http-password=bugzilla_password

#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FNLD9-i386-CD1.iso&buildid=fUNiOCkq1qA~&fileid=AgbPjY19ufw~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FNLD9-i386-CD2.iso&buildid=fUNiOCkq1qA~&fileid=Db69qxCeCxA~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FNLD9-i386-CD3.iso&buildid=fUNiOCkq1qA~&fileid=q5U8ZOPqY5I~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FNLD9-i386-SP1-CD1.iso&buildid=fUNiOCkq1qA~&fileid=snP5LHuc3vE~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FNLD9-i386-SP1-CD2.iso&buildid=fUNiOCkq1qA~&fileid=YobK92HDOLo~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD1.iso&buildid=fUNiOCkq1qA~&fileid=0tE2uaI9eP0~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD2.iso&buildid=fUNiOCkq1qA~&fileid=a735frHR_wY~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD3.iso&buildid=fUNiOCkq1qA~&fileid=OARNisUjXtY~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD4.iso&buildid=fUNiOCkq1qA~&fileid=IHV9Wiskh2Y~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD5.iso&buildid=fUNiOCkq1qA~&fileid=V5lj7eej3Rw~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-i386-RC5-CD6.iso&buildid=fUNiOCkq1qA~&fileid=l4kuM0IInoU~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-SP-1-NLPOS-9-RC13-CD1.iso&buildid=fUNiOCkq1qA~&fileid=EvcQB7NMUu0~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-SP-1-NLPOS-9-RC13-CD2.iso&buildid=fUNiOCkq1qA~&fileid=vGK8-TGe3Cs~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-SP-1-NLPOS-9-RC13-CD3.iso&buildid=fUNiOCkq1qA~&fileid=d4JDhiVN3sc~&mirror=AkamaiHost&nohost=false"
#			"http://download.novell.com/sendredirect?target=%2Fprot%2FfUNiOCkq1qA%7E%2FSLES-9-SP-1-NLPOS-9-RC13-CD4.iso&buildid=fUNiOCkq1qA~&fileid=74GHCoGaZj4~&mirror=AkamaiHost&nohost=false"


		SLEPOS_ISO=(
			"ftp://cml.suse.cz/install/iso/SLES9/NLPOS/SLES-9-NLPOS-9-RC13-CD3.iso"
			"ftp://cml.suse.cz/install/iso/SLES9/NLPOS/SLES-9-NLPOS-9-RC13-CD4.iso"
			"ftp://cml.suse.cz/install/iso/SLES9/NLPOS/SLES-9-SP-2-NLPOS-9-SSP-2.iso"
			"ftp://cml.suse.cz/install/iso/SLES9/NLPOS/SLES-9-SP-3-NLPOS-9-SSP-3-RC2.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-9-i386-FCS-candidate-9-CD1.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-9-i386-FCS-candidate-9-CD2.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-9-i386-FCS-candidate-9-CD3.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-SP-3-i386-RC4-CD1.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-SP-3-i386-RC4-CD2.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-NLD-SP-3-i386-RC4-CD2.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-SP-3-i386-RC4-CD1.iso"
			"ftp://schnell.suse.de/CD-ARCHIVE/SLES9/iso/SLES-9-SP-3-i386-RC4-CD3.iso"
			"ftp://cml.suse.cz/sync/NLD-9-SP4-RC4/SLES-9-NLD-9-SP4-i386-Build00410-CD1.iso"
			"ftp://cml.suse.cz/sync/NLD-9-SP4-RC4/SLES-9-NLD-9-SP4-i386-Build00410-CD2.iso"
			"ftp://cml.suse.cz/sync/NLD-9-SP4-RC4/SLES-9-NLD-9-SP4-i386-Build00410-CD3.iso"
			"ftp://cml.suse.cz/sync/NLD-9-SP4-RC4/SLES-9-NLD-9-SP4-i386-Build00410-CD4.iso"
			"ftp://cml.suse.cz/sync/NLD-9-SP4-RC4/SLES-9-NLD-9-SP4-i386-Build00410-CD5.iso"
		)

		SLES_ISO=(
			"ftp://cml.suse.cz/install/iso/SLES9/SLES-9-i386-RC5-CD1.iso"
			"ftp://cml.suse.cz/install/iso/SLES9/SLES-9-i386-RC5-CD5.iso"
			"ftp://cml.suse.cz/install/iso/SLES9/SLES-9-i386-RC5-CD6.iso"
		)

		# where are located SLEPOS templates for kiwi image building
		SLEPOS_TEMPLATE_PATH="/usr/share/kiwi/image/SLEPOS"

		# path, where are located image definitions and chroots
		IMAGE_PATH="/opt/SLES/POS/dist/myImages"
		# where are located images after its creation?
		IMAGE_SOURCE_PATH="/opt/SLES/POS/image"
		# where should boot images be located on admin server to be distributed to branch servers?
		BOOT_IMAGE_TARGET_PATH="/opt/SLES/POS/rsync/boot"
		# where should system images be located on admin server to be distributed to branch servers?
		SYSTEM_IMAGE_TARGET_PATH="/opt/SLES/POS/rsync/image"
		# where should system images be located on image server?
		BRANCH_IMAGE_PATH="/tftpboot/image/"
		;; # end of definitions for NLPOS 9
esac

if [ -z "$CONF_PATH" ]; then
	CONF_PATH=/usr/share/qa/qa_test_slepos
fi
# with this you can create your own values to override configuration above
# it's meant for full hamsta automation
if [ -f /root/hamsta_slepos_config ]; then
	source /root/hamsta_slepos_config
fi

