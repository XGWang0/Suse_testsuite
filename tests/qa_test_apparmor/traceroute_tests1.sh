#!/bin/sh
################################################################################
##                                                                            ##
## Copyright (c) International Business Machines  Corp., 2001                 ##
##                                                                            ##
## This program is free software;  you can redistribute it and#or modify      ##
## it under the terms of the GNU General Public License as published by       ##
## the Free Software Foundation; either version 2 of the License, or          ##
## (at your option) any later version.                                        ##
##                                                                            ##
## This program is distributed in the hope that it will be useful, but        ##
## WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ##
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License   ##
## for more details.                                                          ##
##                                                                            ##
## You should have received a copy of the GNU General Public License          ##
## along with this program;  if not, write to the Free Software               ##
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA    ##
##                                                                            ##
################################################################################
#
# File :         traceroute_tests.sh
#
# Description:   Test Basic functionality of traceroute command.
#                Test #1: execute traceroute on $address, expected number of
#                hops is 1.
#
# Author:        Manoj Iyer, manjo@mail.utexas.edu
#
# History:       Mar 03 2003 - Created - Manoj Iyer.
#
# Function:     chk_ifexists
#
# Description:  - Check if command required for this test exits.
#
# Input:        - $1 - calling test case.
#               - $2 - command that needs to be checked.
#
# Return:       - zero on success.
#               - non-zero on failure.

address=130.57.66.10
chk_ifexists()
{
    RC=0

    which $2 > $LTPTMP/tst_traceroute.err 2>&1 || RC=$?
    if [ $RC -ne 0 ]
    then
        tst_brkm TBROK NULL "$1: command $2 not found."
    fi
    return $RC
}


# Function: init
#
# Description:  - Check if command required for this test exits.
#               - Create temporary directories required for this test.
#               - Initialize global variables.
#
# Return:       - zero on success.
#               - non-zero on failure.
init()
{
    # Initialize global variables.
    export RC=0
    export TST_TOTAL=2
    export TCID="traceroute"
    export TST_COUNT=0

    # Inititalize cleanup function.
    trap "cleanup" 0

    # create the temporary directory used by this testcase
    if [ -z $TMP ]
    then
        LTPTMP=/tmp/tst_traceroute.$$
    else
        LTPTMP=$TMP/tst_traceroute.$$
    fi

    mkdir -p $LTPTMP > /dev/null 2>&1 || RC=$?
    if [ $RC -ne 0 ]
    then
         tst_brkm TBROK "INIT: Unable to create temporary directory"
         return $RC
    fi

    # check if commands tst_*, traceroute, awk exists.
    chk_ifexists INIT tst_resm   || return $RC
    chk_ifexists INIT traceroute || return $RC
    chk_ifexists INIT awk        || return $RC
    chk_ifexists INIT head       || return $RC
    chk_ifexists INIT cat        || return $RC
    chk_ifexists INIT diff       || return $RC
    chk_ifexists INIT iptables   || return $RC
 
    # Create expected file.
    cat > $LTPTMP/tst_traceroute.exp <<-EOF || RC=$?
traceroute to 130.57.66.10 (130.57.66.10), 4 hops max, 60 byte packets
	EOF

    if [ $RC -ne 0 ]
    then
        tst_brkm TBROK  NULL \
            "INIT: unable to create expected file $LTPTMP/tst_traceroute.exp"
        return $RC
    fi
    return $RC
}


# Function:     cleanup
#
# Description:  - remove temporaty files and directories.
#
# Return:       - zero on success.
#               - non-zero on failure.
cleanup()
{
    # remove all the temporary files created by this test.
    tst_resm TINFO "CLEAN: removing $LTPTMP"
    rm -fr $LTPTMP
}


# Function:     test01
#
# Description:  - Test that traceroute $address will trace route of an IP
#                 packet to that host.
#
# Return:       - zero on success.
#               - non-zero on failure.
test01()
{
    TCID=traceroute01
    TST_COUNT=1
    nhops=0             # Number of hops required to get to host.
    RC=0                # Return value from commands.

    tst_resm TINFO "Test #1: Execute traceroute on www.suse.com."
    tst_resm TINFO "Test #1: traceroute returns the path taken by IP packet"
    tst_resm TINFO "Test #1: to that host."

    traceroute -m 4 $address > $LTPTMP/tst_traceroute.out 2>&1 || RC=$?
    if [ $RC -ne $Flag ]
    then
        tst_res TFAIL $LTPTMP/tst_traceroute.out \
            "Test #1: traceroute command failed: return = $RC. Details:"
        return $RC
    fi

    cat $LTPTMP/tst_traceroute.out | head -n 1 > $LTPTMP/tst_traceroute.out.1 2>&1
    diff -iwB $LTPTMP/tst_traceroute.out.1 $LTPTMP/tst_traceroute.exp \
        > $LTPTMP/tst_traceroute.err 2>&1 || RC=$?
    if ([ $RC -ne 0 ] && [ $Flag -eq 0 ])
    then
        tst_res TFAIL $LTPTMP/tst_traceroute.err \
            "Test #1: unexpected output. Details:"
        return $RC
    elif [ $Flag -eq 0 ]
    then 
         # Only one hop is required to get to $address.
        nhops=$(cat $LTPTMP/tst_traceroute.out | tail -n 1 | awk '{print $1}')
        if [ $nhops -lt 1 ]
        then
            tst_resm TFAIL "Test #1: $hops number of hops unexpected"
        else
            tst_resm TPASS \
                "Test #1: traceroute $address traced route correctly"
        fi
    else 
        tst_resm TPASS \
                "Test #1: traceroute $address blocked by iptables"
    fi

    return $RC
}

# Function:    setiptables
#
# Description:    - save iptables chain and set new iptables chain
#
# Exit:         - zero on success

#               - non-zero on failure.
setiptables()
{
  iptables-save >/root/iptables.save
  if [ $RC -ne 0 ]
  then
      tst_res TFAIL $LTPTMP/tst_traceroute.out \
       "Test #1: save iptables configure file failed: return = $RC. Details:"
      return $RC
  fi

  iptables -F
  if [ $RC -ne 0 ]
  then
      tst_res TFAIL $LTPTMP/tst_traceroute.out \
       "Test #1: clean iptables rules failed: return = $RC. Details:"
      return $RC
  fi

  iptables -A OUTPUT -p udp -j DROP
  if [ $RC -ne 0 ]
  then
      tst_res TFAIL $LTPTMP/tst_traceroute.out \
       "Test #1: set iptables rules failed: return = $RC. Details:"
      return $RC
  fi
}


# Function:    restoreiptables
#
# Description:    - Restore previous settings
#
# Exit:         - zero on success

#               - non-zero on failure.

restoreiptables()
{
  iptables-restore /root/iptables.save
  if [ $RC -ne 0 ]
  then
      tst_res TFAIL $LTPTMP/tst_traceroute.out \
       "Test #1: failed to restore the configuration: return = $RC. Details:"
      return $RC
  fi

  rm -rf /root/iptables.save
}


# Function:    revertresult
#
# Description:    - Revert the result value.
#
# Exit:            - zero on success
#               - non-zero on failure.

revertresult()
{
  if [ $RC -ne 0 ]
  then
      RC=0
  else
      RC=1
  fi
}



# Function:    main
#
# Description:    - Execute all tests and report results.
#
# Exit:            - zero on success
#               - non-zero on failure.
Flag=0
RC=0
init || exit $?

test01 || exit $?
setiptables || exit $?
Flag=1
test01 
RC=$?
revertresult
  
restoreiptables || exit $?
exit $RC
