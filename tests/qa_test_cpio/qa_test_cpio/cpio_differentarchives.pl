#!/usr/bin/perl

#sub cleanup {
#	
#	`rm -r /tmp/archive /tmp/unpacked`
#	
#}

my @formats = ("bin", "odc", "newc", "crc", "tar", "ustar", "hpbin", "hpodc");
my $testdatadir = "/usr/share/qa/qa_test_cpio/data";

`mkdir /tmp/archive`;
foreach $format (@formats) {

	`cd $testdatadir/topack && ls | cpio -o -H $format -O /tmp/archive/test_$format 2>/dev/null`;

}

`mkdir /tmp/unpacked`;
foreach $format (@formats) {
	
	`cd /tmp/unpacked; mkdir $format; cd $format; cpio -i -H $format -I /tmp/archive/test_$format 2>/dev/null`;

}


foreach $format (@formats) {

	$result = `diff  $testdatadir/topack /tmp/unpacked/$format 2>&1`;

	if ($result ne "") {

		print "FAILED: cpio - Test different archive formats\n";
		`rm -r /tmp/archive /tmp/unpacked`;
		exit(1);
	}

}	

print "PASSED: cpio - Test different archive formats\n";
`rm -r /tmp/archive /tmp/unpacked`;
exit(0);

