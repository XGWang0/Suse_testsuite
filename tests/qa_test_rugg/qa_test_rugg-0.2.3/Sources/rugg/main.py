#!/usr/bin/env python
# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@xprima.com>
# License   : GNU Public License <http://www.gnu.org/licenses/gpl.html>
# Creation  : 15-Feb-2006
# Last mod  : 17-Mar-2006
# History   :
#             10-Apr-2006 - Added help command and accompanying text
#             17-Mar-2006 - Important update of the type system.
#             03-Mar-2006 - Moved most functions to the `rugg.core` module
#             27-Feb-2006 - Introduced limited bufffer in data writing size
#             23-Feb-2006 - Improved producers
#             22-Feb-2006 - Integrated words file, better fd management.
#             21-Feb-2006 - SubZones now inherit read and write fd from parent
#             20-Feb-2006 - Updated implementation to conform to test cases
#             17-Feb-2006 - Introduced SubZone and Producers
#             16-Feb-2006 - Preliminary Zone implementation
#             15-Feb-2006 - First implementation
#
# -----------------------------------------------------------------------------

import os, sys, cmd, readline, time
from rugg.language import parseString, parseFile, runString, runFile, operations

__version__ = "0.2.3"

__doc__ = """\
This is the main Rugg module, it contains the definition for the command line
interprter and parser.

For more details on Rugg internals, you should look at the @rugg.language
module, which contains the most important part of the language (parser and
semantics). The @rugg.core module contains the Python API that can be used in
scripts, and this API is wrapped in the @rugg.operations module.
"""

USAGE = """\
Rugg v%s - Hard drive harness and testing language

Rugg is both a tool that allows to create simple to complex scenarios that will
test your hard drive. Rugg scenarios can be written in a compact and expressive
language that allow you to create test that will mimic behaviours of programs
like Apache or PosgreSQL in minutes.

By default, Rugg is started as an interactive shell, unless you giveit some
arguments. You can give paths to files containing scenarios as well as strings
representing program data. To have a list of available command-line options, run
rugg with the "-h" or "--help" options.

Welcome to Rugg ! 
""" % (__version__)

HELP = """\

Syntax overview:
  
  QUANTITY      [NUMBER](b, Kb, Mb, Tb)         10.5Mb
  RANGE         [QUANTITY]..[QUANTITY]          1Mb..10Mb
                [QUANTITY]..[QUANTITY]/STEPS    1Mb..10Mb/10
                [QUANTITY]..[QUANTITY]/INC      1Mb..10Mb+0.5Mb

  OPERATION     [NAME] PARAMETER...             zone 10Mb

  COMBINATION   [EXPRESSION] , [EXPRESSION]     zone 10Mb, subdivide
  ITERATION     [EXPRESSION] : [EXPRESSION]     zone 10Mb, subdivide : fill
  APPLICATION   [EXPRESSION] | [EXPRESSION]     zone 10Mb, subdivide | fill
  GROUPING      ( [EXPRESSION] )                subdivide : (blank, fill)

  COMMENTS      !-- [ANYTHING] --!              !-- Here is a comment --!
""" 

# TODO: Complete with the function names
class Interpreter(cmd.Cmd):
  """Default implementation for the Rugg interpreter."""
  
  def __init__( self ):
    cmd.Cmd.__init__(self)
    self.prompt = "Rugg >> "
    self.intro  = USAGE

  def onecmd( self, string ):
    if string.strip() == "exit" or string=="EOF":
      if string == "EOF": print
      print "Bye !"
      sys.exit(0)
    if string.strip() == "help":
      env = operations.Environment()
      env.register()
      print HELP
      print "Available operations (name and signatures):\n"
      for n, ms in env.listOperations():
        sig = []
        for m in ms: sig.extend(map(str, m[1]._signatures))
        print "  %13s : %s" % (n, ", ".join(sig))
      print
    else:
      runString(string)

# ------------------------------------------------------------------------------
#
# MAIN
#
# ------------------------------------------------------------------------------

OPT_TREE  = "Displays the parse tree."
OPT_CHECK = "Checks the program syntax and semantics."
OPT_NOCLEANUP = "Does not clean the created zone that were not unlinked."

def run( args ):
  # When no argument is given, we enter interactive mode
  if not args:
    Interpreter().cmdloop()
  # Otherwise we interpret the given strings or scenario files
  else:
    try:
        from optparse import OptionParser
    except:
        print "Rugg non-interactive command line requires at least Python 2.3"
        sys.exit(-1)
    # We create the option parser the options
    oparser = OptionParser(version="Rugg " + __version__)
    oparser.prog = "Rugg v%s" % (__version__)
    oparser.add_option("-p", "--parse-tree", action="store_true", dest="parsetree",
      help=OPT_TREE)
    # Interpreter mode options
    oparser.add_option("-c", "--check", action="store_true", dest="check",
      help=OPT_CHECK)
    # Interpreter mode options
    oparser.add_option("-n", "--nocleanup", action="store_true", dest="nocleanup",
      help=OPT_NOCLEANUP)
    # We parse the options and arguments
    (options, args ) = oparser.parse_args(args=args)
    for arg in args:
      program = None
      start_time = time.time()
      if not os.path.exists(arg):
        program = parseString(arg, display=options.parsetree, run=not options.check)
      else:
        program = parseFile(arg, display=options.parsetree, run=not options.check)
      if program and program.succeeded and not options.check:
        print "Finished in %0.3fs." % ( time.time() - start_time)
      if program and options.check: print "Program", args, "is valid."
      # If the program did not succeed, we return a -1 status
      if program and not options.nocleanup: program.cleanup()
      if not program or not program.succeeded \
      or program.environment._errors > 0:
        sys.exit(-1)

if __name__ == "__main__":
  run(sys.argv[1:])

# EOF
