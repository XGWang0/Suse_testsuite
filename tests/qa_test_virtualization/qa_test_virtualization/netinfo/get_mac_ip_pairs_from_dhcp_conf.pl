#!/usr/bin/perl -w
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#


my $conf_file = "/etc/dhcpd.conf";

sub find_mac_ip
{
	my ($s) = @_;

	if ($s =~ /hardware\s+ethernet\s+([0-9a-f:]+);/i) {
		my $mac = $1;
		print "$mac $1\n" if $s =~ /fixed-address\s+([0-9.]+);/i;
	}
}

open CONF, "<", $conf_file or die "Cannot open file $conf_file for reading.\n";

my $str = "";
for (<CONF>) {
	chomp;
	s/#.*$//;
	next if /^\s*$/;
	$str .= $_ . " ";
	print $_ . "\n";
}


while ($str =~ s/(\{[^{}]*\})/=BRACKET=;/) {
	# now we have the most internal block, values are plitted by semicolon
	# if we find mac& ip here, print it (no other than host block can have it
	# and we replace the block by =BRACKET=;, so we can recurse again
	find_mac_ip($1);
};

# process the rest (it should not print anything, but who knows ;-)
find_mac_ip($str);

