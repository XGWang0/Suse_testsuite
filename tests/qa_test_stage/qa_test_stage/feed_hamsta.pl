#!/usr/bin/perl -w
# vim: set et ts=4 sw=4 ai si:
#
# feed_hamsta -- command line interface for the hamsta master
#

use strict;
use Getopt::Long qw(:config no_ignore_case bundling_override);
use POSIX qw(strftime WIFEXITED WEXITSTATUS WIFSIGNALED WTERMSIG WIFSTOPPED WSTOPSIG);
# handle HUP INT PIPE TERM ABRT QUIT with die, so the END block is executed
# which unlinks temporary files
use sigtrap qw(die untrapped normal-signals ABRT QUIT);
use Encode;

use IO::Socket::INET;

#to get result from hamsta
use LWP::Simple;

$0 =~ m/([^\/]*)$/;
my $progname = $1;

# Make sure output is in UTF8
binmode(STDOUT, ":utf8");

my $debug = 0;

my $cvs_id = '$Id: feed_hamsta.pl 1586 2006-12-22 11:39:17Z kwolf $';
my $cvs_date = '$Date: 2006-12-22 12:39:17 +0100 (Fri, 22 Dec 2006) $';
$cvs_id =~ /^\$[[:alpha:]]+: [^ ]+ ([^ ]+ [^ ]+ [^ ]+) ([^ ]+ )?[^ ]+ \$$/;
my $version = $1;

#my $tmpfile = "/tmp/$progname.$$";
#END { unlink($tmpfile); }

# Usage message
sub usage {
    print <<"EOF";
$progname version $version

$progname [OPTIONS] <master>[:<port>]

Options:
    -c|--command <command>  send the given command to the master and print 
                            the returned message
    -p|--print-active       print all active machines
    -j|--job <filename>     send a job to the client specified by the -h or
                            -g option (<filename> is not local but on the
                            master)
    -h|--host <ip>          set the target host for -j
    -g|--group <name>       set the target host group for -j
    -v|--version            print program version
    -d|--debug <level>      set debugging level (defaults to $debug)
       --help               print this help message
EOF
}

my $opt_help            = 0;
my $opt_version         = 0;
my $opt_w		= 0;

my $opt_command         = "";
my $opt_print_active    = 0;
my $opt_job             = "";
my $opt_host            = "";
my $opt_group           = "";

# parse command line options
unless (GetOptions(
           'help'               =>  \$opt_help,
           'version|v'          =>  \$opt_version,
           'wait|w'             =>  \$opt_w,
           'debug|d=i'          =>  \$debug,
           'command|c=s'        =>  \$opt_command,
           'job|j=s'            =>  \$opt_job,
           'host|h=s'           =>  \$opt_host,
           'group|g=s'          =>  \$opt_group,
           'print-active|p'     =>  \$opt_print_active,
          )) {
  &usage ();
  exit 1;
}

if ($opt_version) {
  print "$progname version $version\n";
  exit 0;
}

if ($opt_help) {
  &usage ();
  exit 0;
}

if ($#ARGV != 0) {
  print "Please specify the master to connect to.\n\n";
  &usage ();
  exit 1;
}

my $opt_master;
my $opt_master_port;

($opt_master, $opt_master_port) = split(/:/, $ARGV[0]);
$opt_master_port = 18431 unless $opt_master_port;

print "Connecting to master $opt_master on $opt_master_port\n";
    
my $sock;
eval {
    $sock = IO::Socket::INET->new(
        PeerAddr => $opt_master,
        PeerPort => $opt_master_port,
        Proto    => 'tcp'
    );
};
if ($@ || !$sock) {
    print "Could not connect to master: $@$!\n";
    exit 2;
}

# Ignore the welcome message and wait for the prompt
&send_command('');

#catch the jop id
my $job_id="";
if ($opt_command) {
    $job_id=&send_command($opt_command."\n");
    print $job_id;

    # if -w then wait for the job result
    if($opt_w) {

	exit 0 unless($job_id=~/internal id/);

	$job_id =~ s/.*internal id:.//;	
	$job_id =~ s/[^d]$//g;
	my $url="http://$opt_master/hamsta/index.php?go=job_details&id=$job_id";
	my $result_job="";
	while($result_job eq "running" or $result_job eq "queued" or $result_job eq "") {
		my $content = get $url;
		my @content = split /\n/,$content;
		for(my $i=0;$i<@content;$i++){
			
			if($content[$i] =~ />Status</){
				$i++;
				$result_job = $content[$i];
				$result_job =~ s/.*<td>//;
				$result_job =~ s/<\/td>.*//;
				#print $result_job,"\n";
				last;
			}
		}
		sleep 3;
	}
	exit 0 if($result_job=~"passed");
	exit 1 if($result_job!~"passed");
	}
}

if ($opt_print_active) {
    print &send_command("print active\n");
}

if ($opt_job) {
    if ($opt_host && $opt_group) {
        print "Please specify either a host or a group of hosts, not both.\n\n";
        exit 1;
    }

    if ($opt_host) {
        print &send_command("send job ip $opt_host $opt_job\n");
    } elsif ($opt_group) {
        print &send_command("send job group $opt_group $opt_job\n");
    } else {
        print "Please specify a host or a group of hosts.\n\n";
        exit 1;
    }
}


sub send_command() {
    my $cmd = shift;
    my $result = "";
    my $line = "";
    
    eval {
        if ($cmd) {
            $sock->send($cmd);
            print "Sent $cmd" if $debug > 0;
        }
    };
    if ($@) {
        print "Message could not be send: $@\n";
        exit 2;
    }

    print "Recv " if $debug > 1;
    while (1) {
        $_ = $sock->getc(); 
        if ($_ eq '') {
            print "Master possibly terminated our session. Please restart.\n";
            exit 2;
        }
        
        print $_ if $debug > 1;
        $line .= $_;
        
        if ($_ eq "\n") {
            $result .= $line;
            $line = "";
        }

        print "Recv " if ($_ eq "\n") && ($debug > 1);
        
        last if ($line =~ /\$>/);
    }
    print "\n" if $debug > 1;

    return $result;
}
