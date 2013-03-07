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
def generate( f, l ): env.generate(f,l)

__doc__ = "Ensures that the File object works properly."

if __name__ == "__main__":
  path = os.path.splitext( os.path.abspath(__file__))[0] + ".zone"
  # Creates file with a given size and ensures that the size is right
  fl = File(path)
  assert fl.size() == 0, "Wrong file size: %s != %s" % (fl.size(), 0)
  generate(fl, 0)
  assert fl.size() == 0, "Wrong file size: %s != %s" % (fl.size(), 0)
  generate(fl, 100)
  assert fl.size() == 100, "Wrong file size: %s != %s" % (fl.size(), 100)
  generate(fl, 256)
  assert fl.size() == 356, "Wrong file size: %s != %s" % (fl.size(), 356)
  generate(fl, 1)
  assert fl.size() == 357, "Wrong file size: %s != %s" % (fl.size(), 357)
  fl.unlink()
  # Creates file with a given size and ensures that the size is right
  fl = File(path)
  assert fl.size() == 0, "Wrong file size: %s != %s" % (fl.size(), 0)
  generate(fl, 0)
  assert fl.size() == 0, "Wrong file size: %s != %s" % (fl.size(), 0)
  generate(fl, KB(16))
  assert fl.size() == KB(16), "Wrong file size: %s != %s" % (fl.size(), KB(16))
  generate(fl, KB(16))
  assert fl.size() == KB(32), "Wrong file size: %s != %s" % (fl.size(), KB(32))
  fl.wseek(0)
  generate(fl, KB(11))
  generate(fl, KB(21))
  assert fl.size() == KB(32), "Wrong file size: %s != %s" % (fl.size(), KB(32))
  fl.unlink()
  # Creates files with size limits and ensure that the size is right
  fl = File(path, KB(96))
  assert fl.size() == 0, "Wrong file size: %s != %s" % (fl.size(), 0)
  generate(fl, KB(96))
  assert fl.size() == KB(96), "Wrong file size: %s != %s" % (fl.size(), KB(96))
  try:
    generate(fl, KB(16))
    assert None, "An exception should have been raised, because we have " + \
    "reached the file limit."
  except OperationalError:
    pass
  assert fl.size() == KB(96), "Wrong file size: %s != %s" % (fl.size(), KB(96))
  fl.wseek(0)
  generate(fl, KB(96))
  assert fl.size() == KB(96), "Wrong file size: %s != %s" % (fl.size(), KB(96))
  fl.wseek(200)
  generate(fl, KB(96) - 200) 
  assert fl.size() == KB(96)
  fl.unlink()
  print "OK"

# EOF
