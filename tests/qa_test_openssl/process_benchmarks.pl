#!/usr/bin/perl

use strict;
use warnings;

my $count = 5;
my $i = 0;
my $j = 0;
my $max = 0;
my $position = 0;
my @results = ();

if( @ARGV < $count) {
	print "usage: scanfile.pl filename1 filename2 filename3 filename4 filename5\n";
	exit 0;
}

for($i = 0; $i < $count; $i++) {
	open my $file, '<', $ARGV[$i] or die "Cannot open file \"$ARGV[$i]\"";
	$results[$i] =  [ parse_input($file) ];
	close $file;
}

# for each result file get the value and compare it, take only the best one
for $i (0 .. $#{$results[0]}) {
	$position = 0;
	$max = 0;
	for $j ( 0 .. $#results ) {
		if ($max < get_value($results[$j][$i])) {
			$max = get_value($results[$j][$i]);
			$position = $j;
		}
	}
	print get_text($results[$position][$i]);
}

sub get_text
{
	my $lne = shift;

	my ($val, $text);
	if ($lne =~ /^(\d+) (.*)/) {
		($val,$text)=($1,$2);
	}
	return $text . "\n";   
}

sub get_value
{
	my $lne = shift;

	my ($val, $text);
	if ($lne =~ /^(\d+) (.*)/) {
		($val,$text)=($1,$2);
	}
	return $val;   
}

sub parse_input
{
	# scan each file
	# for each file calculate our value
	# if there is not escape match then line value is 0 and we can use it from any file.

	my $file = shift;
	my @results=();

	my ($size, $test, $frame, $val, $optype);
	while( my $row=<$file> ) {
		if ($row =~ /Doing (.+?)('s)?\W+for (\d+)s: (\d+) (.+?)\W+/) {
			($frame,$val)=($3,$4);

			push @results, sprintf "%d %s", $val/$frame, $row;
		} elsif ($row =~ /^Doing (.+?)('s)?\W+for (\d+)s on (\d+) size blocks: (\d+)/) {
			($frame,$size,$val)=($3,$4,$5);

			push @results, sprintf "%d %s", ($val/$frame*$size)/1024, $row;
		} else {
			push @results, "0 ". $row;
		}
	}

	return @results;
}
