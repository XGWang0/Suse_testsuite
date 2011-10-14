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

package Test;
require 5.002;
use strict;

my @tv = (
# test name, options, input, expected output, expected return code
#
['idem-0', '', "", "", 0],
['idem-1', '', "a", "a", 0],
['idem-2', '', "\n", "\n", 0],
['idem-3', '', "a\n", "a\n", 0],

['basic-0-10', '',
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n0\n",
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n0\n", 0],

['basic-0-09', '',
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n",
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n", 0],

['basic-0-11', '',
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n0\nb\n",
 "1\n2\n3\n4\n5\n6\n7\n8\n9\n0\n", 0],

['obs-0', '-1', "1\n2\n", "1\n", 0],
['obs-1', '-1c', "", "", 0],
['obs-2', '-1c', "12", "1", 0],
['obs-3', '-14c', "1234567890abcdefg", "1234567890abcd", 0],
['obs-4', '-2b', [\'in'], [\'in-1024'], 0],
['obs-5', '-1k', [\'in'], [\'in-1024'], 0],

# This test fails for textutils-1.22, because head let 4096m overflow to 0
# and did not fail.  Now head fails with a diagnostic.

# Disable this test because it fails on systems with 64-bit longs.
# ['fail-0', '-n 4096m', "a\n", "", 1],

# In spite of its name, this test passes -- just to contrast with the above.
['fail-1', '-n 2048m', "a\n", "a\n", 0],

# Make sure we don't break like AIX 4.3.1 on files with \0 in them.
['null-1', '', "a\0a\n", "a\0a\n", 0],

# Make sure counts are interpreted as decimal.
# Before 2.0f, these would have been interpreted as octal
['no-oct-1', '-08',  "\n"x12, "\n"x8, 0],
['no-oct-2', '-010', "\n"x12, "\n"x10, 0],
['no-oct-3', '-n 08', "\n"x12, "\n"x8, 0],
['no-oct-4', '-c 08', "\n"x12, "\n"x8, 0],

);

sub test_vector
{
  my @derived_tests;
  foreach my $t (@tv)
    {
      my ($test_name, $flags, $in, $exp, $ret) = @$t;

      # Derive equivalent, posix-style tests from the obsolescent ones.
      next if $test_name !~ /^obs-/;

      $test_name =~ s/^obs-/posix-/;
      if ($flags =~ /-(\d+)$/)
	{
	  $flags = "-n $1";
	}
      elsif ($flags =~ /-(\d+)([cbk])$/)
	{
	  my $suffix = $2;
	  $suffix = '' if $suffix eq 'c';
	  $flags = "-c $1$suffix";
	}
      else
	{
	  $flags = "-l $`";
	}
      push (@derived_tests, [$test_name, $flags, $in, $exp, $ret]);
    }

  foreach my $t (@tv, @derived_tests)
    {
      my ($test_name) = @$t;
      $Test::input_via{$test_name} = {REDIR => 0, FILE => 0, PIPE => 0}
    }

  return (@tv, @derived_tests);
}

1;
