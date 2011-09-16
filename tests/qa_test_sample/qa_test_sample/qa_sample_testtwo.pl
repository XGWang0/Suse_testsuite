#!/usr/bin/perl

$dirName = "thisdir";

# Make sure we are on i*86 (I know, this makes no sense, but it is only for demo purposes)
$arch = `arch`;
unless($arch =~ m/^i.86\s$/)
{
	print "You are not running i*86, so skipping this test.\n";
	exit (22);
}

# See if /$dirName doesn't yet exist
if ( -d "/$dirName" ) {
	print "Oops! /$dirName already was there. No idea what to do now. Bye!\n";
	exit (11);
}

# Create /$dirName
mkdir("/$dirName",0777);

# Now make sure /$dirName exists
if ( -d "/$dirName" ) {
	print "Yes! /$dirName was successfully created!\n";
	exit (0);
} else {
	print "Oops! /$dirName could not be created. That is unfortunate. Perhaps either you are not root, or your file system is really messed up. Bye!\n";
	exit (1);
}
