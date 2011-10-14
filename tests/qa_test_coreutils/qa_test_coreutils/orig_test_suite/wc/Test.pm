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

$Test::input_via_stdin = 1;

my @tv = (
# test flags  input                 expected output        expected return code
['a0', '-c',  '',                   "0\n",                          0],
['a1', '-l',  '',                   "0\n",                          0],
['a2', '-w',  '',                   "0\n",                          0],
['a3', '-c',  'x',                  "1\n",                          0],
['a4', '-w',  'x',                  "1\n",                          0],
['a5', '-w',  "x y\n",              "2\n",                          0],
['a6', '-w',  "x y\nz",             "3\n",                          0],
# Remember, -l counts *newline* bytes, not logical lines.
['a7', '-l',  "x y",                "0\n",                          0],
['a8', '-l',  "x y\n",              "1\n",                          0],
['a9', '-l',  "x\ny\n",             "2\n",                          0],
['b0', '',    "",                   "0 0 0\n",                      0],
['b1', '',    "a b\nc\n",           "2 3 6\n",                      0],
['c0', '-L',  "1\n12\n",            "2\n",                          0],
['c1', '-L',  "1\n123\n1\n",        "3\n",                          0],
['c2', '-L',  "\n123456",           "6\n",                          0],
);

sub test_vector
{
  my $t;
  foreach $t (@tv)
    {
      my ($test_name, $flags, $in, $exp, $ret) = @$t;
      # By default, test both stdin-redirection and input from a pipe.
      $Test::input_via{$test_name} = {REDIR => 0, PIPE => 0};

      # But if test name ends with `-file', test only with file arg(s).
      # FIXME: unfortunately, invoking wc like `wc FILE' makes it put
      # FILE in the ouput -- and FILE is different depending on $srcdir.
      $Test::input_via{$test_name} = {FILE => 0}
        if $test_name =~ /-file$/;

      # Now that `wc FILE' (note, with no options) produces results
      # different from `cat FILE|wc', disable those two `PIPE' tests.
      $flags eq ''
	and delete $Test::input_via{$test_name}->{PIPE};
    }

  return @tv;
}

1;
