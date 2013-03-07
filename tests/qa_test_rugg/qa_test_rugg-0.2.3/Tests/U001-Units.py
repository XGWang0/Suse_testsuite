#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.core import *

__doc__ = "Ensures that the units are properly parsed."

GOOD_UNITS = (
  ("10",           10),
  ("10b",          10),
  ("10B",          10),
  ("10.0",         10),
  ("10.0b",        10),
  ("10.0B",        10),
  ("10.1B",        10),
  ("10Mb",         MB(10)),
  ("10MB",         MB(10)),
  ("10mB",         MB(10)),
  ("10MB",         MB(10)),
  ("10.1Mb",       MB(10.1)),
  ("0.1Mb",        MB(0.1)),
  ("10Gb",         GB(10)),
  ("10GB",         GB(10)),
  ("10gB",         GB(10)),
  ("10GB",         GB(10)),
  ("10.1Gb",       GB(10.1)),
  ("0.1Gb",        GB(0.1)),
)

BAD_UNITS = (
  "10.0.0",
  "10Xb",
  "10 Mb"
)

if __name__ == "__main__":
  for text, result in GOOD_UNITS:
    print "Parsing ", text
    assert result == parseSize(text), "Expected %s, got %s" % (result, parseSize(text))
  for text in BAD_UNITS:
    print "Parsing ", text
    assert None   == parseSize(text), "Expected None, got %s" % (parseSize(text))
  print "OK"

# EOF
