#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.language import *

__doc__ = "Ensures that the units are properly parsed."

# These expressions are syntactically valid, but are not always semantically
# valid
VALID_EXPRESSIONS = """\
zone 50Mb
zone 50Mb, blank
zone 50Mb, blank, fill
zone 50Mb, fill random
zone 50Mb, subdivide 2
zone 50Mb, subdivide 2, fill random
zone 50Mb, subdivide 2, fill random, join

zone 50Mb, subdivide 2 : fill random
zone 50Mb, subdivide 2 : blank : fill random
zone 50Mb, subdivide 2 : fill random, blank

zone 50Mb, subdivide 2 : fill same random : blank : fill same random
zone 50Mb, subdivide 2 : (fill same random , blank) : fill same random
zone 50Mb, (subdivide 2 : (fill same random , blank)) : fill same random

"""

RANGES = """
10kb..50kb/50  : zone 
10kb..50kb+5kb : zone 
"""

MULTILINES = [

"""\
zone 50Mb,
  blank,
  fill
""",

"""zone
50Mb
, blank, fill"""
]

COMMENTS = [

"""\
# zone 50Mb, blank, fill
zone 50 Mb, fill
""",

]
if __name__ == "__main__":
  for expression in VALID_EXPRESSIONS.split("\n"):
    print ">>", expression
    if not expression: continue
    res = parseString(expression, validate=False)
    print res
    assert res, "Cannot parse " + expression
  for expression in RANGES.split("\n"):
    print ">>", expression
    if not expression: continue
    res = parseString(expression, validate=False)
    print res
    assert res, "Cannot parse " + expression
  for expression in MULTILINES:
    print ">>", expression
    res = parseString(expression, validate=False)
    assert res, "Cannot parse " + expression
  for expression in COMMENTS:
    print ">>", expression
    res = parseString(expression, validate=False)
    print res
    assert res, "Cannot parse " + expression
  print "OK"
# EOF
