#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.core import *
from rugg.operations import Environment

env = Environment(None)

def blank( f ): env.blank(f)

__doc__ = "Ensures that filling a zone creates the proper amount of bytes."

if __name__ == "__main__":
  path = os.path.splitext( os.path.abspath(__file__))[0] + ".zone"
  sizes = (10, 100, MB(1), MB(10), MB(100))
  for size in sizes:
    zone = Zone(path, size)
    blank(zone)
    assert zone.size () == size, "%s != %s" % (zone.size(), size)
    zone.unlink()
  print "OK"

# EOF
