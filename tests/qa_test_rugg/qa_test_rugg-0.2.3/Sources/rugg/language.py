#!/usr/bin/env python
# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre                           <sebastien@xprima.com>
# License   : GNU Public License         <http://www.gnu.org/licenses/gpl.html>
# Creation  : 27-Feb-2006
# Last mod  : 04-May-2006
# History   : 
#             04-May-2006 - Changed comment to '#' instead of '!-- --!', updated
#                           error printing to better support multi-line scripts.
#             10-Avr-2006 - Added multi-line scripts and comment support. Update
#             the ranges to allow specifying a step in quantity.
#             03-Avr-2006 - Added Nothing filtering in args.
#             24-Mar-2006 - Small changes to the grammar, added support for the
#             repetition combinator.
#             21-Mar-2006 - Added program 'succeeded' state and 'isrunning' for
#             current task.
#             20-Mar-2006 - Support for context, indicating whether an iteration
#             is sequential or parallel.
#             16-Mar-2006 - Added Rugg typecast-made types (this is a big
#             update)
#             12-Mar-2006 - Implemented application (with threads), added steps
#             specification to ranges.
#             06-Mar-2006 - Improved error handling, added 'blank' operation.
#             03-Mar-2006 - Implemented basic functions from rugg.core.
#             02-Mar-2006 - Cleaner program model, improved semantics, much
#             better error reporting. Introduced the BLAH token in the grammar
#             to allow more english-like expression.
#             01-Mar-2006 - Enhanced semantics, tree representation
#             28-Feb-2006 - Working TPG grammar and preliminary PyParsing
#             27-Feb-2006 - First implementation
# -----------------------------------------------------------------------------

import sys, os, threading
# This is for the PyParsing parser
#from rugg.pyparsing import nums, alphanums, Literal, Word, Forward, Regex, Group, \
#ZeroOrMore, OneOrMore, Or
# This is for the TPG parser
from rugg import tpg
from rugg import core, typesystem, operations
from rugg.logger import *

def type_format( the_type ):
  """Formats the given type to be printed on a terminal. If the type is UNKNOWN,
  it will be printed in RED, otherwise in GREEN."""
  if the_type == typesystem.Unknown: return format(the_type, color=RED, weight=BOLD)
  else: return format(the_type, GREEN)

# ------------------------------------------------------------------------------
#
# PROGRAM MODEL ELEMENTS
#
# ------------------------------------------------------------------------------

# ELEMENT ______________________________________________________________________

class Element:
  """Element is the abstract class for components of the program model.
  
  Attributes:
                children        [Element]
                errors          [Exception]
                token           tpg.Token
  """

  def __init__(self, *args):
    self.children = []
    self.errors   = []
    self.token    = None
    self.parent   = None
    # We do not use extend, because subclasses may redefine add
    for a in args: self.add(a)

  def add( self, element ):
    self.children.append(element)
    element.parent = self

  def type( self ):
    """Returns the type for this element."""
    return typesystem.Nil

  def annotateChild( self, child, index ):
    """Allows to annotate the child element at the given index. For instance, the
    first child of an operation is called the "operation name", then the rest
    are arguments. This allows this information to be printed on the tree."""
    return ""

  def asString( self ):
    """Returns a string representing the element.
    NOTE: When you subclass this function, make sure it never fails, as the
    Program tree must be printed when an exception has occured, to let the user
    know what went wrong with the program."""
    return self.__class__.__name__ + ":" + type_format(self.type())
  
  def errorsAsString( self ):
    """Returns a string containing all the errors for this element. This will be
    printed with the element in its string representation."""
    res = "\n".join([format("!"+e.args[0], RED, BOLD) for e in self.errors])
    return res

  def error( self, exception ):
    """Declares that an error was detected with this element, and adds it to the
    'errors' attribute of this element."""
    self.errors.append(exception)

  def validate( self, markOnly=False ):
    """Ensures that the element is semantically consistent. A typical use is to
    check if the arguments given to a function are of the proper type. When a
    problem occurs, a SemanticException can be raised."""
    for c in self.children:c.validate(markOnly)

  def run( self, program, arguments=() ):
    """Runs the element as being part of the given program. This leads to the
    execution of the declaration represented in the program model. It does
    nothing by default."""
    program.running = self
    for c in self.children:
      c.run(program)

  def __str__( self ):
    """This function prints the element and all its descendants as a nicely
    formatted tree."""
    text  = "%s\n" % ( self.asString() )
    err   = self.errorsAsString()
    if err: text += err + "\n"
    if self.children:
      ci   = 0
      for child in self.children:
        annotation = self.annotateChild(child, ci)
        if annotation: annotation = " (%s)" % ( annotation)
        first_line = True
        last_child = child == self.children[-1]
        ci        += 1
        for line in str(child).split("\n"):
          if not line: continue
          if first_line:
            if not last_child:
              text += "├──" + line + annotation + "\n"
            else:
              text += "└──" + line + annotation + "\n"
            first_line = False
          else:
            if not last_child:
              text += "│  " + line + "\n"
            else:
              text += "   " + line + "\n"
    return text

# PROGRAM ______________________________________________________________________

class Program(Element):
  """Represents a Rugg program as a whole. The program has a stack of values,
  representing the current context (which is a value). The stack can be
  manipulated by the program builder."""

  def __init__(self):
    Element.__init__(self)
    # We instanciante an operating environment
    self.environment = operations.Environment(self)
    self.environment.register()
    # This is the stack that holds the stacks of values (contexts)
    self.stack = []
    # This is the zones creates in this program
    self.zones = []
    # This is the status of the program, wether it has failed or not
    self.succeeded = False
    # Indicates the element that is currently running
    self.running   = None

  def add( self, element ):
    if element == None: return
    assert isinstance(element, ProgramElement)
    element.program(self)
    Element.add(self, element)

  def type( self ):
    """Returns the type for this element."""
    if not self.children: return typesystem.Unknown
    return self.children[-1].type().result()

  def run( self, program=None, arguments=() ):
    self.environment.start()
    #try:
    if True:
      Element.run(self, program or self, arguments)
    #except Exception, e:
    #  self.environment.error(e)
    #  raise e

  def createZone( self, *args, **kwargs ):
    """Creates a Zone which will be initialized with the given arguments."""
    zone = core.Zone(*args, **kwargs)
    self.zones.append(zone)
    return zone

  def cleanup( self ):
    """Unlinks all zones registered in this program."""
    for z in self.zones: z.unlink()

# PROGRAM ELEMENT ______________________________________________________________

class ProgramElement(Element):
  """An element that belong to a particular program."""

  def __init__(self, program, *args):
    Element.__init__(self)
    self.program(program)
    for arg in args: self.add(arg)

  def program( self, program=None ):
    """Sets/gets the program associated to this element."""
    if program:
      self._program = program
      for c in self.children: c.program(program)
    return self._program

  def add( self, element ):
    element.program(self.program())
    Element.add(self, element)

# VALUE ________________________________________________________________________

class Value(ProgramElement):
  """A value represents elements that can be directly converted to values, and
  can be processed by operations. Values do not have children.
  
  Attributes:
              value           Element|str
              children        ()
  """

  def __init__( self, program, value ):
    """Creates a value that wraps the given (Python) value"""
    ProgramElement.__init__(self, program)
    self.value = value
    self.children = ()

  def asString(self): return  format(self.value, CYAN) \
      + ":" + format(self.__class__.__name__ , GREEN)

  def run(self,program, args=()):
    return self.value

# STRING ________________________________________________________________________

class String(Value):
  """Rerpresents a string."""
  def type(self): return typesystem.String

# QUANTITY ______________________________________________________________________

class Quantity(Value):
  """Represents a quantity."""
  def type(self): return typesystem.Quantity
  def run(self, program, args=()): return core.parseSize(self.value)

# PARAMETER ______________________________________________________________________

class Parameter(Value):
  """A Parameter is a value that is produced by the enclosing compositor. For
  instance, the iteration on a range will add a number parameter to the given
  operation."""

  def __init__( self, program, _type ):
    Value.__init__(self, program, None) ; self._type = self.value = _type

  def type(self): return self._type

  def asString(self): return  format(self.__class__.__name__ , BLACK) \
      + ":" + type_format(self.value)

# SYMBOL _________________________________________________________________________

class Symbol(Value):
  """A Symbol is a string that represents an element of the program, wether
  available in the program context, or available in the internal program
  runtime. Symbols are typically used to represent functions by their names, so
  Symbols are simply strings."""
  def type(self): return typesystem.Symbol

# RANGE _________________________________________________________________________

class Range(Value):
  """A Range is a set of values (and is also a value)."""

  def type(self):
    return typesystem.Array(typesystem.Quantity)

  def run(self, program, args=()):
    program.running = self
    # Parse the arguments
    minval, maxval = self.value.split("..")
    steps = 10
    increment = None
    # The Range can be suffixed by
    # /[NUMBER] to indicate the number of items in the resulting range
    # +[QUANTITY] to indicate the increment
    if maxval.rfind("/") > 0: maxval, steps     = maxval.split("/")
    if maxval.rfind("+") > 0: maxval, increment = maxval.split("/")
    minval = core.parseSize(minval)
    maxval = core.parseSize(maxval)
    steps  = int(steps)
    if increment: increment = core.parseSize(increment)
    # Creates the interval
    # If no increment was specified, then we divide in steps
    if increment == None:
      step   = (max(maxval,minval) - min(maxval, minval)) / float(steps)
      value  = min(maxval, minval)
      values = [value]
      while steps > 2:
        value += step
        values.append(long(round(value)))
        steps -= 1
      values.append(max(maxval, minval))
      if not maxval == max(maxval, minval): values.reverse()
    # Otherwise we simply use the incrementation method
    else:
      start = min(minval, maxval)
      end   = max(minval, maxval)
      while start <= end:
        values.append(start)
        start += increment
    return values

# OPERATION ______________________________________________________________________

class Operation(ProgramElement):
  """An operation is an ProgramElement that can produce a value, by doing something. An
  operation has an associated _context_ (which one could also called the local
  environment) that contains data passed by enclosing operations.
  
  Attributes:
                context                 [Value]
  An operation has no assertion on its children.
  """
  def __init__( self, program, *args ):
    """Initializes this operation, which will have a blank context by default."""
    self.context = []
    ProgramElement.__init__(self, program, *args)

  def contextAdd( self, element ):
    """Adds a value to this operation context."""
    assert isinstance(element, Value),"Only values can be added to the context."
    self.context.append(element)

  def contextType( self ):
    """Returns the type for this operation context."""
    if not self.context:
      return typesystem.Nothing
    if len(self.context) == 1:
      return self.context[0].type()
    else:
      return apply(typesystem.Arguments, tuple(v.type() for v in self.context))

# INVOCATION __________________________________________________________________

#@structure("Symbol,Any*")
class Invocation(Operation):
  """An invocation is the operation that will look into the Rugg language
  functions, take the function, and invoke the function with the parameters
  found in the invocation context.
  
  An invocation is (SYMBOL, ANY*)
  """

  def name( self ):
    """Returns the function name for this invocation"""
    return self.children[0].value

  def argumentsType( self ):
    """The invocation arguments are the children following the first child."""
    if len(self.children) > 2:
      return typesystem.makeArguments(tuple(c.type() for c in self.children[1:]))
    elif len(self.children) == 2:
      return self.children[1].type()
    else:
      return typesystem.Nothing

  def inputType( self ):
    """The input type is the type of the arguments, plus the type of the
    context. So this is basically equal to PROCESS(argumentsType,
    contextType)."""
    r = typesystem.combineArguments(self.argumentsType(), self.contextType())
    return r

  def type( self ):
    """The type of an invocation corresponds to the processing of the context
    type, returning the corresponding type defined in the FUNCTIONS table."""
    p = typesystem.Process()
    p.arguments(self.inputType())
    try:
      r = self.program().environment.returnType(self.name(), self.inputType())
    except operations.OperationDoesNotRespond, e:
      r = typesystem.Unknown
    p.result(r)
    return p

  def validate( self, markOnly=False ):
    try:
      self.program().environment.returnType(self.name(), self.inputType())
    except operations.OperationDoesNotRespond, e:
      if not markOnly: raise e
      else: self.error(e)
    Operation.validate(self, markOnly=True)

  def run( self, program, parameters=() ):
    """Runs this invocation in the given program."""
    program.running = self
    args = list([x.run(program) for x in self.children[1:]])
    args.extend(parameters)
    # We filter out the Nothing singleton
    args = list(a for a in args if a != typesystem.Nothing)
    # No element of the argument should be a program model element
    assert not filter(lambda x:isinstance(x,ProgramElement), args)
    try:
      res = self.program().environment.invoke(self.name(), self.inputType(), args)
    except Exception, e:
      a = [] ; a.extend(e.args)
      e.args = a 
      e.args[0]  = e.args[0] + " in operation '%s'" % (self.name())
      raise e
    return res

  def __str__( self ):
    """This function prints the element and all its descendants as a nicely
    formatted tree."""
    text  = ""
    err   = self.errorsAsString()
    if err: text += err + "\n"
    if self.children:
      text += format(" ".join(tuple(str(c.value) for c  in self.children)),
      weight=BOLD)
    text += ":" + type_format(self.type())
    return text

# ITERATION ___________________________________________________________________

#@structure("(Value|Operation):[ANY], Operation")
class Iteration(Operation):
  """An iteration sequentially applies the elements of a SET value as parameter
  to the context of the given operation.

  Structure: VALUE|OPERATION, OPERATION
  where the VALUE or value returned by the first OPERATION is a SET.
  """

  def add( self, element ):
    Operation.add(self, element)
    if len(self.children) == 1:
      pass
    else:
      if self.children[0].type().result().isSubtypeOf(typesystem.Array):
        _type = self.children[0].type().result().content()
      else:
        _type = typesystem.Unknown
      element.contextAdd(Parameter(self.program, _type))

  def contextAdd( self, element ):
    """When an element is added to the iteration context, it will be added to
    the combination first child context."""
    if self.children and not isinstance(self.children[0], Value):
      # We modify the context of the first children
      self.children[0].contextAdd(element)
      # Which has an effect on the type of the next children
      if len(self.children) == 2:
        if len(self.children[1].context) == 1:
          self.children[1].context[0] = Parameter(self.program(), self.children[0].type().result().peel())
        else:
          # FIXME: There may be problem here
          pass

  def type( self ):
    res = self.children[1].type().result()
    if res != typesystem.Nothing:
      return typesystem.Array(res)
    else:
      return res

  def validate( self, markOnly=False ):
    input_type = self.children[0].type().result()
    if not input_type.isSubtypeOf(typesystem.Array):
      Operation.validate(self, markOnly=True)
      exception = typesystem.SemanticError("First value/operation should raise an Array instead of '%s'" % (input_type), self)
      if not markOnly: raise exception
      else: self.error(exception)
    else:
      Operation.validate(self, markOnly)

  def run( self, program, parameters=() ):
    """Runs this by iterating through the values raised by the first operation,
    and applying them to the second."""
    program.running = self
    result = []
    # We notify the environment of the start of a parallel execution. This
    # allows the operations to properly react, depending on the type of
    # iterations. This was made necessary by the 'fill same' implementation,
    # which is not the same when in sequential or in parallel modes.
    elements = self.children[0].run(program, parameters)
    self.program().environment.startContext(mode="sequential", elements=elements)
    for value in elements:
      p = [value]
      p.extend(parameters)
      result.append(self.children[1].run(program, p))
    self.program().environment.endContext()
    return result

# APPLICATION _________________________________________________________________

class Application(Iteration):
  """An Application is a specific kind of Iteration, where the application of
  the values of the SET to the operation is made in parallel, not in
  sequence."""

  def run( self, program, parameters=() ):
    """Runs this by iterating through the values raised by the first operation,
    and applying them to the second."""
    program.running = self
    result  = []
    threads = []
    # The results is guarded by a lock
    result_lock = threading.Lock()
    def thread_runner(child, a, b):
      # We run the given funcition (it is a program element)
      try:
        v = child.run(a, b)
        result_lock.acquire()
        result.append(v)
        result_lock.release()
      except Exception, e:
        self.program().environment.error("During operation: %s" % (child))
        self.program().environment.error(e)
    # We notify the environment of the start of a parallel execution. This
    # allows the operations to properly react, depending on the type of
    # iterations. This was made necessary by the 'fill same' implementation,
    # which is not the same when in sequential or in parallel modes.
    elements = self.children[0].run(program, parameters)
    self.program().environment.startContext(mode="parallel", elements=elements)
    for value in elements:
      p = [value]
      p.extend(parameters)
      t = threading.Thread(target=thread_runner, args=(self.children[1], program, p))
      threads.append(t)
      t.start()
    remaining = len(threads) - 1
    for t in threads:
      t.join()
      remaining -=1
    self.program().environment.endContext()
    return result

# REPETITION __________________________________________________________________

class Repetition(Operation):
  """A repetition "absorbs its first argument", and repeats the attached
  operation the number of time described by the first argument."""

  def add( self, element ):
    Operation.add(self, element)
    assert len(self.children) <= 2

  def type( self ):
    return typesystem.Array(self.children[1].type().result())

  def validate( self, markOnly=False ):
    input_type = self.children[0].type().result()
    if not isinstance(self.children[0], Quantity) and \
       not isinstance(self.children[0], Range):
      Operation.validate(self, markOnly=True)
      exception = typesystem.SemanticError("Expected QUANTITY or RANGE as argument.")
      if not markOnly: raise exception
      else: self.error(exception)
    else:
      Operation.validate(self, markOnly)


  def run( self, program, parameters=() ):
    """Runs this by iterating through the values raised by the first operation,
    and applying them to the second."""
    program.running = self
    result          = []
    self.program().environment.startContext(mode="sequential")
    count           = self.children[0].run(program)
    if type(count) in (tuple, list): count = len(count)
    for i in range(count):
      result.append(self.children[1].run(program, parameters))
    self.program().environment.endContext()
    return result

# COMBINATION _________________________________________________________________

class Combination(Operation):
  """A combination makes a "chain" of operations, where the first element may be
  either a value or operation. The result of the previous operation is then
  passed as a parameter to the next one.

  Structure: (VALUE|OPERATION, OPERATION...)
  If the first element is a VALUE, then the combination context should not be
  modified, because the first child will inherit the combination context --
  which will only work if the first element is an operation (values have no
  context).
  """

  def add( self, element ):
    Operation.add(self, element)
    # If the element is the first child, it will take its context from the
    # combination
    if len(self.children) == 1:
      for v in self.context: element.contextAdd(v)
    # If the child is not the first child, then it is an operation, and we set
    # its type to be the type of the previous operation
    else:
      if not isinstance(element, Operation):
        raise typesystem.SemanticError("Expected Operation, but got %s" %
        (element.__class__.__name__), self)
      _type = self.children[-2].type().result()
      element.contextAdd(Parameter(self.program(), _type))

  def contextAdd( self, element ):
    """When an element is added to the combination context, it will be added to
    the combination first child context."""
    if self.children and not isinstance(self.children[0], Value):
      # We modify the context of the first children
      self.children[0].contextAdd(element)
      # Which has an effect on the type of the next children
      for i in range(1, len(self.children)):
        assert len(self.children[i].context) == 1
        self.children[i].context[0] = Parameter(self.program(), 
          self.children[i-1].type().result())

  def type( self ):
    # FIXME: Ensure that context is empty if first child is value
    return typesystem.Process(self.contextType(),
      self.children[-1].type().result())

  def run( self, program, parameters=() ):
    """Runs each child sequentially, by feeding the preceding one the result of
    the next."""
    program.running = self
    for c in self.children:
      res = c.run(program, parameters)
      # We only add thre result to the parameters if it is not None
      parameters = [res]
      if res != None: parameters = [res]
      else: parameters = []
    if parameters:
      return parameters[0]
    else:
      return None

# ------------------------------------------------------------------------------
#
# PROGRAM BUILDER
#
# ------------------------------------------------------------------------------

#@states(NO_PROGRAM, PROGRAM_CREATED)
#@substate(PROGRAM_CREATED, IN_OPERATION)
class ProgramBuilder:
  """The ProgramBuilder is the main interface, drive by the parser, to create
  Rugg programs. You can also drive the ProgramBuilder "by hand" to build Rugg
  program from Python scripts.
  
  NOTE: program builders are not threadsafe, which means that you cannot share a
  single program builder instance between different threads. Create a new one
  instead for each thread."""

  #@state(NO_PROGRAM)
  def __init__( self ):
    """Initializes the program builder."""
    self.program   = None
    self.parser    = None
    self.inComment = False

  def startComment( self ):
    self.inComment = True

  def endComment( self ):
    self.inComment = False

  #@when(NO_PROGRAM)
  #@state(PROGRAM_CREATED)
  def createProgram( self, parser ):
    """Creates a new program. You must call `endProgram` before calling
    `createProgram` again."""
    self.program = Program()
    self.parser  = parser
    return Program()

  def setOffsets( self, element ):
    """Sets the offsets of the given element. This is automatically called on
    the element creation."""
    if element.token == None: element.token = self.parser.mark()
    # FIXME: ProgramElement token information should be set here
    return element

  #@when(PROGRAM_CREATED)
  def endProgram( self ):
    """Ends the current program, and returns the `Program` instance that was
    created by the `createProgram` call."""
    res = self.program
    self.program = self.parser = None
    return res

  #@when(PROGRAM_CREATED)
  def createRange( self, _range ):
    """Creates and returns a new Range element, and adds it to the program
    stack."""
    r = Range(self.program, _range) 
    self.program.stack.append(r)
    self.setOffsets(r)
    return r

  def createString( self, word ):
    """Creates a Word value."""
    r = String(self.program, word)
    self.program.stack.append(r)
    return self.setOffsets(r)

  def createQuantity( self, quantity ):
    """Creates a Quantity value."""
    r = Quantity(self.program, quantity)
    self.program.stack.append(r)
    return self.setOffsets(r)

  #@when(PROGRAM_CREATED)
  #@state(IN_OPERATION)
  def createInvocation( self, name ):
    assert type(name) == str
    o = Invocation(self.program, Symbol(self.program, name))
    self.setOffsets(o)
    self.program.stack.append(o)
    return o

  #@when(IN_OPERATION)
  def endOperation( self ):
    return None

  #@when(PROGRAM_CREATED)
  def createIteration( self, element ):
    r = Iteration(self.program, element)
    self.program.stack.append(r)
    return self.setOffsets(r)

  #@when(PROGRAM_CREATED)
  def createApplication( self, element ):
    r = Application(self.program, element)
    self.program.stack.append(r)
    return self.setOffsets(r)

  #@when(PROGRAM_CREATED)
  def createRepetition( self, element ):
    r = Repetition(self.program, element)
    self.program.stack.append(r)
    return self.setOffsets(r)

  #@when(PROGRAM_CREATED)
  def createCombination( self, element ):
    if isinstance(element, Combination): return element
    r = Combination(self.program, element)
    self.program.stack.append(r)
    return self.setOffsets(r)

# We create a shared instance of the program builder
builder = ProgramBuilder()

# ------------------------------------------------------------------------------
#
# PARSERS
#
# ------------------------------------------------------------------------------

class Parser(tpg.VerboseParser):
  r"""
    separator  space   '[\s\n]+';
    separator  comment '#.+';

    token BLAH       'with|to|in|it|that|the|they|of|is|are';
    token RANGE      '\d+(\w+)?\.\.\d+(\w+)?(/\d+|\+\d+\w+)?';
    token QUANTITY   '\d+(\.\d+)?(\w\w|\%)?';
    token WORD       '\w[\w\d]+';
    token LPAREN     '\(';
    token RPAREN     '\)';
    token COMMA      '\,';
    token COLON      '\:';
    token PIPE       '\|';
    token STAR       '\*';
    token COMMENT_S  '\!\-\-';
    token COMMENT_E  '\-\-\!';

    START/s       ->  $ s = builder.createProgram(self)
                      Expression/e 
                      $ s.add(e)
                      $ builder.endProgram()
                      ;
    Range/r       ->  RANGE/r
                      $ r = builder.createRange(r)
                      ;
    Operation/o   ->  WORD/w
                      $ o = builder.createInvocation(w)
                      ( BLAH 
                      | WORD/w     $ o.add(builder.createString(w))
                      | QUANTITY/q $ o.add(builder.createQuantity(q))
                      | RANGE/r    $ o.add(builder.createRange(r))
                      ) *
                      $ builder.endOperation()
                      ;

    Atom/a        ->  QUANTITY/a  $ a = builder.createQuantity(a)
                      | Range/a
                      | Operation/a
                      | LPAREN Expression/a $ a = a $ RPAREN
                      ;

    Expression/a  ->  Atom/a
                      (
                        ( COLON $ a = builder.createIteration(a)
                        | PIPE  $ a = builder.createApplication(a)
                        | COMMA $ a = builder.createCombination(a)
                        | STAR  $ a = builder.createRepetition(a)
                        )
                        Atom/b
                        $ a.add(b)
                      )*
                      ;


  """
  verbose = 0
  def lineForPos(self, pos=None):
    """Returns (LINENUM, LINETEXT, LINEPOS) where LINENUM is the line number of
    the given position in the parsed text, LINETEXT the line text, and LINEPOS
    the position relatively to the start of the line."""
    if pos == None: pos = self.lexer.pos
    text = self.lexer.input
    sol  = max(text[:pos].rfind("\n"), 0)
    line = text[:pos].count("\n")
    eol  = sol + text[pos:].find("\n")
    if eol == -1: eol = len(text)
    current_line = text[sol:eol]
    current_pos  = pos - sol
    return line, current_line, current_pos

def createParser():
  """Creates the parse for the Rugg mini language. This is an internal method
  that creates a TPG or PyParsing parser."""
  return Parser()

PARSER = createParser()

def printError( name, description, pos=None, pos_end=None ):
  """Helper function used by parseString to report when an error has occured."""
  lnum, ltext, lpos = PARSER.lineForPos(pos)
  ltext = ltext.replace("\n", " ")
  if pos_end:
    lend = lpos + pos_end - pos
  else:
    lend = ltext.find(" ", lpos) 
    if lend == -1: lend = len(ltext) 
  if lend == lpos: lpos -= 1
  print format("%s at line %s: " % (name, lnum), RED) + description
  head = ">>> " 
  print format(head, RED) +format(ltext[:lpos], GREEN) + \
  format(ltext[lpos:lend], RED, BOLD) + format(ltext[lend:], GREEN)
  print " " * ( len(head) + lpos ) + format("^"*(lend-lpos), RED)

def parseString( text, run=False, validate=True, display=False ):
  """Parses the given string of text and returns an object model representing
  the program."""
  program   = None
  try:
    program = PARSER(text)
    if validate: program.validate()
    if display: print program
    if run: program.run()
    program.succeeded = True
    return program
  # TODO: Intercept Syntactic Errors
  # This kind of error happens when the given expression had a bad syntax
  except tpg.LexicalError, e:
    printError("Lexical error", e.msg)
    return None
  except tpg.SyntacticError, e:
    printError("Syntax error", e.msg)
    return None
  # This error happens when the semantic of the epxression is not proper
  # (for instance, when the types of operations do not match)
  except typesystem.SemanticError, e:
    message = e.args[0]
    element = e.args[-1]
    if element and element.token:
      printError("Semantic error", message, element.token.start,
      element.token.stop)
      element.error(e)
    else:
      printError("Semantic error", e)
    print program
    return program
  # This happens when there is an error when executing the operations. This
  # is most probably due to a failure in the implementation of the language,
  # and not because of the user.
  except typesystem.RuntimeError, e:
    if program and program.running: 
      printError(e.__class__.__name__, str(e), program.running.token.start,
      program.running.token.stop)
    else:
      printError(e.__class__.__name__, str(e))
    return program
  # This is the MOST IMPORTANT kind of errors, as the whole purpose of Rugg
  # is to be able to generate those errors, which indicate that there was a
  # problem with the disk.
  except core.FileError, e:
    printError(e.__class__.__name__, str(e), program.running.token.start,
    program.running.token.stop)
    return program

def parseFile( path, run=False, validate=True, display=False):
  """Parses the give file."""
  assert os.path.exists(path)
  f = file(path, "r")
  t = f.read()
  f.close()
  return parseString(t, run, validate, display)

def runString( text ): return parseString(text, True)
def runFile( text ): return parseFile(text, True)

# ------------------------------------------------------------------------------
#
# MAIN
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
  args = sys.argv[1:]
  if not args:
    print "Please give a string or a file path as argumnet."
  for arg in args:
    if not os.path.exists(arg):
      print "Parsing string '%s'" % (arg)
      print parseString(arg)
    else:
      print "Parsing file '%s'" % (arg)
      print parseFile(arg)

# EOF
