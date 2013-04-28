#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

__doc__ = """Ensures that creating and filling subzones does not change a zone
size"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.core import *
from rugg.operations import Environment

env = Environment(None)
def generate( f, l ): env.generate(f,l)
def blank( f ): env.blank(f)
def ensure( f ): env.ensureSame(f)
def fill( f, *args, **kwargs ):
  if type(f) in (list, tuple):
    for z in f: env.fill_typeWithZones(z, *args, **kwargs)
  else:
    env.fill(f, *args, **kwargs)

if __name__ == "__main__":
  path = os.path.splitext( os.path.abspath(__file__))[0] + ".zone"
  sizes = (100, 1000, 10000, 100000, MB(1), MB(10))
  for size in sizes:
    print "Creating zone of",size,"bytes"
    zone = Zone(path, size)
    blank(zone)
    # For each size, we create from 2 to 10 subzones
    for i in range(2,10):
      zone.seek(0)
      assert zone.size() == size, "Zone has not the expected size: %s != %s" % (
      zone.size(), size)
      subzone_size = zone.size() / i
      print "  Dividing zone in",i,"subzones of", subzone_size,"bytes"
      # We divide the zone and fill each subzone with random text
      subzones = zone.subdivide(i)
      assert zone.size() == size, "Zone has not the expected size: %s != %s" % (
      zone.size(), size)
      fill(zone.subzones(), producer=randomTextProducer)
      # Ensures that each subzone has the proper size
      for subzone in subzones:
        assert subzone.size() == zone.size() / i, "Subzone size is %s != %s" % (
        subzone.size(), zone.size() / i )
        print "  subzone sig", subzone.sig(), len(subzone.data())
      # Ensures that every subzone has the same data
      # assert ensure(zone.subzones()), "Zones are not identical"
      # We join the zone so we can divide it again
      zone.join()
      assert zone.size() == size, "Zone size has changed inbetween %s != %s" % (zone.size(), size)
    zone.unlink()
  print "OK"

# EOF
