#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.language import *
from rugg import core

__doc__ = """Ensure that the program semantics are properly implemented by making
small programs and verifying their results."""


print "Creating 50Mb zone"
program = parseString("zone 50Mb", validate=True, run=True)
assert len(program.zones) == 1
assert program.zones[0].size() == 0
program.cleanup()

print "Creating 50Mb zone, and blanking"
program = parseString("zone 50Mb, blank", validate=True, run=True)
assert len(program.zones) == 1
assert program.zones[0].size() == core.MB(50), program.zones[0].size()
program.cleanup()

print "Creating 50Mb zone, and filling"
program = parseString("zone 50Mb, fill", validate=True, run=True)
assert len(program.zones) == 1
assert program.zones[0].size() == core.MB(50), program.zones[0].size()
program.cleanup()

print "Creating 50Mb zone, subdivide in 2 and fill"
program = parseString("zone 50Mb, subdivide 2, blank", validate=True, run=True)
assert len(program.zones) == 1
assert len(program.zones[0].subzones()) == 2
assert program.zones[0].size() == core.MB(50), program.zones[0].size()
program.cleanup()

print "OK"

# EOF

