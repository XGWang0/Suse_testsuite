# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@xprima.com>
# License   : GNU Public License <http://www.gnu.org/licenses/gpl.html>
# Creation  : 16-Mar-2006
# Last mod  : 17-Mar-2006
# History   : 17-Mar-2006 - Merged in exceptions
#             16-Mar-2006 - First implementation
# -----------------------------------------------------------------------------

from rugg import typecast 

# ------------------------------------------------------------------------------
#
# BASIC TYPE DEFINITIONS
#
# ------------------------------------------------------------------------------

# Symbolic types
Nothing   = typecast.Nothing
Nil       = typecast.Nil
Any       = typecast.Any
Unknown   = typecast.Symbolic("#")
Symbol    = typecast.Symbolic("Symbolic")
Quantity  = typecast.Symbolic("Quantity")
Range     = typecast.Symbolic("Range")
Zone      = typecast.Symbolic("Zone")
#TODO: Maybe also do SubZone
String    = typecast.Symbolic("String")

# Composite types
Process   = typecast.Process
Array     = typecast.Array
Sequence  = typecast.Sequence
Arguments = typecast.Arguments

# Utility functions
def makeArguments( args ): return typecast.Sequence_make(args, Arguments)
def combineArguments( a, b ):return typecast.Sequence_combine(a, b, Arguments)

# ------------------------------------------------------------------------------
#
# EXCEPTIONS
#
# ------------------------------------------------------------------------------

class RuggError(Exception): pass
class SemanticError(RuggError): 
  """An exception that is thrown when a semantic error was detected."""
class RuntimeError(RuggError): 
  """An exception that is thrown when a runtime error was detected."""
  pass
class UndefinedOperation(RuntimeError): pass
class OperationDoesNotRespond(RuntimeError): pass

# EOF
