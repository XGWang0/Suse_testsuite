#!/usr/bin/perl -w

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
