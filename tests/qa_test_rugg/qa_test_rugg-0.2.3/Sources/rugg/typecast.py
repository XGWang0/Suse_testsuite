#!/usr/bin/env python
# Encoding: iso-8859-1
# vim: tw=80 ts=4 sw=4 noet
# -----------------------------------------------------------------------------
# Project   : Typecast - Generic type system elements
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@type-z.org>
# License   : BSD Revised License
# Creation  : 09-Mar-2006
# Last mod  : 21-Mar-2006
# History   : 21-Mar-2006 - Sequence combine was not working properly.
#             17-Mar-2006 - Changed the order of arguments in isXXX functions,
#             and renmade _isXXX to isXXX. The methods were reviewed and
#             updated. Implemented isSameAs.
#             16-Mar-2006 - Added Python classes in the isSubtype rules
#             14-Mar-2006 - Renamed Bag to Map, made isSubtype tests work. Added
#             a bunch of test suites and slightly reorganized the modul.
#             13-Mar-2006 - Added isSubtype, Context class, updated Any, Nil.
#             10-Mar-2006 - Added objects, functions, interfaces.
#             09-Mar-2006 - First implementation
# -----------------------------------------------------------------------------

# TODO: Add Logical
# TODO: Implement isSame
# TODO: What about a type (like Parameter) that can be substituted to different
#       types. isSubtype(Parameter, Parameter(String))
# TODO: Test suites for Sequence_combine

import types as pythontypes

__version__   = "0.0.4"
__pychecker__ = "unusednames=_,___,_0_"

# ------------------------------------------------------------------------------
#
# EXCEPTIONS
#
# ------------------------------------------------------------------------------

class SemanticError(Exception): pass

# ------------------------------------------------------------------------------
#
# ABSTRACT TYPE
#
# ------------------------------------------------------------------------------

class Type:
	"""Abstract class for all types."""

	def __init__( self ):
		"""Creates a new anonymous type"""
		self._name = None
	
	def result( self ):
		"""Returns the result for this type. This is usually just the type
		itself, except for processes types."""
		return self
	
	def isSameAs( self, otherType ):
		"""Generic implementation of isSameAs. You should always call this method
		in subclasses."""
		if otherType == self: return True
		else: return False

	def isLike( self, otherType ):
		"""Generic implementation of isLike. You should always call this method
		in subclasses, as it implements basic type systems rules such as
		isLike(Any)."""
		if otherType == self: return True
		if otherType == Any: return True
		return False
	
	def isSubtypeOf( self, otherType ):
		"""Generic implementation of isSubtypeOf. You should always call this method
		in subclasses, as it implements basic type systems rules such as
		isSubtypeOf(Any)."""
		if type(otherType) == pythontypes.ClassType \
		and isinstance(self, otherType): return True
		if otherType == self: return True
		if otherType == Any: return True
		return False
	
	def name( self, name=None):
		"""Returns/sets the name for this type. By defaults, types are unnamed."""
		if name: self._name = name
		return self._name

	def asString( self ):
		"""Returns a string representation of this type."""
		return None

	def __str__( self ):
		assert self.asString() != None, "Method asString not implemented in %s." % \
		(self.__class__.__name__)
		return self.asString()

	# TODO: Add "annotations" or "characteristics"

# ------------------------------------------------------------------------------
#
# SYMBOLIC TYPE
#
# ------------------------------------------------------------------------------

class Symbolic(Type):
	"""Symbolic types are types that have no physical counter part but play a
	role in the type system. This is for instance the case with Any or Nil."""

	def __init__( self, name ):
		Type.__init__(self)
		self._name = name
	
	def asString( self ):
		return self._name

# ------------------------------------------------------------------------------
#
# CELL TYPE
#
# ------------------------------------------------------------------------------

class Cell(Type):
	"""A cell type represents a memory unit. It has a size (in bytes) the
	represents in lenght in memory."""

	def __init__( self, length ):
		Type.__init__(self)
		self._bytes = length

	def isSameAs( self, otherType ):
		if Type.isSameAs(self, otherType): return True
		if not isinstance( otherType, Cell): return False
		return otherType.length() == self.length()

	def isLike( self, otherType ):
		"""The other type is like this Cell if the other type is a cell of the
		same length as this one."""
		if Type.isLike(self, otherType): return True
		if not isinstance( otherType, Cell):
			return False
		if self.length() != otherType.length(): return False
		return True

	def isSubtypeOf( self, otherType ):
		if Type.isSubtypeOf(self, otherType): return True
		if not isinstance( otherType, Cell): return False
		if self.length() >= otherType.length(): return True
		return False

	def length( self ):
		"""Returns the length for this cell."""
		return self._bytes
	
	def asString( self ):
		if self.name(): return self.name()
		else: return "%sb" % (self.length())

# ------------------------------------------------------------------------------
#
# ARRAY TYPE
#
# ------------------------------------------------------------------------------

class Array(Type):
	"""A sequence is simply an ordered set of types."""

	def __init__( self, contentType ):
		Type.__init__(self)
		assert contentType != Nothing, "There is no point in an array of Nothing."
		self._contentType = contentType
	
	def setContentType( self, theType ):
		assert isinstance(theType, Type)
		self._contentType = theType

	# TODO: Maybe add a "peel" method
	def content( self ):
		"""Returns the type for the content of this array."""
		return self._contentType

	def isSameAs( self, otherType ):
		if Type.isSameAs(self, otherType): return True
		if not isinstance( otherType, Array): return False
		return self.content().isSameAs(otherType.content())

	def isLike( self, otherType ):
		"""Othertype must be an Array with a content type that is the same type
		as the content type."""
		if Type.isLike(self, otherType): return True
		if not isinstance(otherType, Array): return False
		return self.content().isLike(otherType.content())
	
	def isSubtypeOf( self, otherType ):
		"""Othertype must be an Array with a content type that is a subtype of
		this content type."""
		if Type.isSubtypeOf(self, otherType): return True
		if not isinstance(otherType, Array): return False
		return self.content().isSubtypeOf(otherType.content())

	def asString( self ):
		return "[%s]" % (self._contentType.asString())

# ------------------------------------------------------------------------------
#
# SEQUENCE TYPE
#
# ------------------------------------------------------------------------------

class Sequence(Type):
	"""A sequence is simply an ordered set of types."""

	def __init__( self, *args ):
		Type.__init__(self)
		self._elements = []
		for arg in args: self.add(arg)
	
	def add( self, theType ):
		assert isinstance(theType, Type)
		assert not self._elements or \
		not self._elements[-1] == Rest, "No element is allowed after Rest"
		self._elements.append(theType)
	
	def extend( self, othertype ):
		if isinstance(othertype, Sequence):
			for e in othertype.elements():
				self.add(e)
		else:
			self.add(othertype)

	def elements( self ):
		return self._elements
	
	def length( self ):
		return len(self._elements)

	def isSameAs( self, otherType ):
		if Type.isSameAs(self, otherType): return True
		if not isinstance( otherType, Sequence): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if len(this_elements) != len(other_elements): return False
		for i in range(min(len(other_elements), len(this_elements))):
			if not this_elements[i].isSameAs(other_elements[i]): return False
		return True

	def isLike( self, otherType ):
		"""The other type is like this one if the other is a sequence with the
		same length and that all elements are like the corresponding elements of
		this sequence."""
		if Type.isLike(self, otherType): return True
		if not isinstance(otherType, Sequence): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		for i in range(min(len(other_elements), len(this_elements))):
			if this_elements[i] == Rest or other_elements[i] == Rest: return True
			if not this_elements[i].isLike(other_elements[i]): return False
		if len(other_elements) != len(this_elements): return False
		return True

	def isSubtypeOf( self, otherType ):
		if Type.isSubtypeOf(self, otherType): return True
		if not isinstance(otherType, Sequence): return False
		this_elements = self.elements()
		other_elements = otherType.elements()
		for i in range(min(len(other_elements), len(this_elements))):
			if this_elements[i] == Rest or other_elements[i] == Rest: return True
			if not this_elements[i].isSubtypeOf(other_elements[i]): return False
		if len(other_elements) > len(this_elements): return False
		return True

	def asString( self ):
		return "(" + ",".join([t.asString() for t in self._elements]) + ")"

def Sequence_make( args, sequenceclass=Sequence ):
	"""Tries to make a sequence from the given argumnents. This follows the
	following rules:

		len(args) == 0         -> Nothing
		len(args) == 1         -> args[1]
		otherwise              -> (args....)
	"""
	if len(args) == 0: return Nothing
	if len(args) == 1: return args[0]
	else: return apply(sequenceclass, args)

def Sequence_combine( a, b, sequenceclass=Sequence ):
	"""Combines the given arguments into a sequence. This follows the following
	rules:
		Nothing, Nothing     -> Nothing
		Nothing, A           -> A
		A,       B           -> (A, B)
		(A, B),  C           -> (A, B, C)   ( type = type(a) )
		(A, B),  (C, D)      -> (A, B, C, D) ( type = type(a) )
		A     ,  (C, D)      -> (A, B, C)   ( type = sequenceclass)
	"""
	if a == Nothing and b == Nothing: return Nothing
	if a == Nothing: return b
	if b == Nothing: return a
	if isinstance(a, Sequence):
		if isinstance(b, Sequence):
			for el in b.elements():
				a.add(element)
		else:
			a.add(b)
		return a
	if isinstance(b, Sequence):
		a = sequenceclass(a)
		for el in b.elements():
			a.add(element)
		return a
	else:
		return sequenceclass(a, b)

# ------------------------------------------------------------------------------
#
# PROCESS TYPE
#
# ------------------------------------------------------------------------------

class Arguments(Sequence): pass
# TODO: Maybe extend sequence ? ==> May pose a problem when subtyping
class Process(Type):
	"""A process generates values by processing (optional) arguments."""

	def __init__( self, *args ):
		Type.__init__(self)
		self._elements = []
		for arg in args: self.add(arg)
		if args: self._ensureIntegrity()

	def _ensureIntegrity(self):
		if not len(self._elements) >= 2:
			raise SemanticError(
			"A process must have at least one argument and a result.")

	def add( self, theType ):
		"""Adds the given type as an element to this process. The last added
		type becomes the result if one type was already added, the argument
		otherwise."""
		assert isinstance(theType, Type)
		self._elements.append(theType)

	def arguments( self, args=None ):
		"""Returns the arguments of this process encapsulated in a sequence
		if there is more than one argument."""
		if args:
			if type(args) in (tuple, list):
				for arg in args:
					self.add(arg)
			else:
				self.add(args)
			return self.arguments()
		else:
			if len(self._elements) == 2:
				return self._elements[0]
			else:
				return apply(Arguments, self._elements[:-1])
	
	def elements( self ):
		return self._elements

	def result( self, result=None ):
		"""If there is not at least 2 addded types, the result is Nothing."""
		if result:
			self.add(result)
			return self.result()
		else:
			self._ensureIntegrity()
			return self._elements[-1]
	
	def peel( self ):
		"""If this process is (A, B)->C, will return (B)->C. You cannot peel a
		process that is (B)->C."""
		if len(self._elements) == 2:
			raise SemanticError("Cannot peel a process with only two elements.")
		return Process(self._elements[1:])

	def isSameAs( self, otherType ):
		if Type.isSameAs(self, otherType): return True
		if not isinstance(otherType, Process): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if not len(this_elements) == len(other_elements): return False
		for i in range(len(this_elements)):
			if not this_elements[i].isLike(other_elements[i]):return False
		return True

	def isLike( self, otherType ):
		"""The other type is like this one if the other is a sequence with the
		same length and that all elements are like the corresponding elements of
		this sequence."""
		if Type.isLike(self, otherType): return True
		if not isinstance(otherType, Process): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if not len(this_elements) == len(other_elements): return False
		for i in range(len(this_elements)):
			if not this_elements[i].isLike(other_elements[i]):return False
		return True

	def isSubtypeOf( self, otherType ):
		"""The other type is like this one if the other is a sequence with the
		same length and that all elements are like the corresponding elements of
		this sequence."""
		if Type.isSubtypeOf(self, otherType): return True
		if not isinstance(otherType, Process): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if  len(this_elements) > len(other_elements): return False
		for i in range(len(this_elements)):
			if not this_elements[i].isSubtypeOf(other_elements[i]):
				return False
		return True

	def asString( self ):
		return self.arguments().asString() + "->" + self.result().asString()

# ------------------------------------------------------------------------------
#
# MAP TYPE
#
# ------------------------------------------------------------------------------

class Map(Type):
	"""A map is simply an unordered set of types, mapped to names."""

	def __init__( self, **kwargs ):
		Type.__init__(self)
		self._elements = {}
		for name,value in kwargs.items():
			self.add(name,value)
	
	def add( self, name, theType ):
		assert isinstance(theType, Type)
		assert theType != Nothing, "There is no point in adding Nothing."
		self._elements[name] = theType

	def elements( self ):
		"""Returns a dict of the elements in this map. Do not modify it."""
		return self._elements
	
	def element( self, key ):
		"""Returns the element associated to the given key."""
		return self._elements[key]

	def isSameAs( self, otherType ):
		if Type.isSameAs(self, otherType): return True
		if not isinstance(otherType, Map): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if len(this_elements.keys()) != len(other_elements.keys()): return False
		for key in this_elements.keys():
			val = other_elements.get(key)
			if val == None: return False
			if not this_elements[key].isSameAs(val): return False
		return True

	def isLike( self, otherType ):
		"""The other type is like this one if the other is a sequence with the
		same length and that all elements are like the corresponding elements of
		this sequence."""
		if Type.isLike(self, otherType): return True
		if not isinstance(otherType, Map): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		if len(this_elements.keys()) != len(other_elements.keys()): return False
		for key in this_elements.keys():
			val = other_elements.get(key)
			if val == None: return False
			if not this_elements[key].isLike(val): return False
		return True

	def isSubtypeOf( self, otherType ):
		"""The other type is a subtype of this one if for each element of this
		type, we find that the other type has a subtype."""
		if Type.isSubtypeOf(self, otherType): return True
		if not isinstance(otherType, Map): return False
		this_elements  = self.elements()
		other_elements = otherType.elements()
		# This type must be longer or equal than the other
		if len(this_elements.keys()) < len(other_elements.keys()): return False
		for key in other_elements.keys():
			val = this_elements.get(key)
			if val == None: return False
			if not val.isSubtypeOf(other_elements[key]): return False
		return True

	def asString( self ):
		return "{" + ",".join(["%s:%s" % (k, t.asString()) for k, t in
		self.elements().items()]) + "}"

# ------------------------------------------------------------------------------
#
# CONTEXT TYPE
#
# ------------------------------------------------------------------------------

class Context(Map):
	"""The Context type is the type that will probably be the most used in OO
	languages. A context can inherit from other contexts, in which case there is
	an explicit subtyping relationship."""

	def __init__( self, *args, **kwargs ):
		Map.__init__(self, **kwargs)
		self._parents = []
		for arg in args:
			assert isinstance(arg, Context)
			self.extends(arg)
	
	def extends( self, parent ):
		"""Add a new parent from which this Context inherits."""
		assert parent not in self._parents
		self._parents.append(parent)

	def elements( self ):
		"""Returns a dict of the elements in this map."""
		e = {}
		# We merge the current and parent elements into the e dict
		for key in self._elements.keys(): e[key] = self._elements[key]
		for parent in self._parents:
			pe = parent.elements()
			for key in pe.keys(): e[key] = pe[key]
		# And return it
		return e
	
	def element( self, key ):
		"""Returns the element associated with the given key, or 'None' if it
		does not exist."""
		if key not in self._elements.keys():
			for parent in self._parents:
				r = parent.element(key)
				if r != None: return r
			return None
		else:
			return Map.element(self, key)

# ------------------------------------------------------------------------------
#
# TYPE ALGEBRA
#
# ------------------------------------------------------------------------------

def bits(size):
	"""Converts the given number of bits into bytes. This is simply for
	readibility purprose."""
	assert size % 8 == 0
	return size / 8

# Creates the basic types of the type system
_True       = lambda a,b: True
_False      = lambda a,b: a == b or False
Nil         = Symbolic("Nil")
Nothing     = Symbolic("Nothing") ; _0_ = Nothing 
Any         = Symbolic("Any")     ; _   = Any
Rest        = Symbolic("...")     ; ___ = Rest
Char        = Cell(bits(8))
Integer     = Cell(bits(32))
LongInteger = Cell(bits(64))
Float       = Cell(bits(64))
LongFloat   = Cell(bits(128)) ; Double = LongFloat
String      = Array(Char)
class Function(Process): pass
class Method(Process): pass
class Object(Context): pass
class Interface(Context): pass
class Class(Context): pass

def isSame( a, b ):
	"""Type (b) is the same as (a) if (a) and (b) are identicial, that means
	that you can use b where you use a, and this also means that isSame(a,b) ==
	isSame(b,a). Basically, when (b) is same as (a), (b) can be considered as an
	alias for (a)."""
	a.isSame(b)

def isLike( a, b ):
	"""Type (b) is like type (a) if (b) can be used where (a) can be used. When
	two types are alike but not the same, this usually means that one type is
	composed at some level of 'Any' or 'Rest' types.
	
	Not that isLike(a,b) does not imply isLike(b,a), as (a) may be a "broad"
	type (such as 'Any'), and (b) a particular type (say 'String')."""
	return a.isLike(b)

def isSubtype( a, b ):
	assert a != None, "Type (a) is None - Only Type instances are accepted."
	assert b != None, "Type (a) is None - Only Type instances are accepted."
	return a.isSubtypeOf(b)

# ------------------------------------------------------------------------------
#
# TEST CASES
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":

	# Here we test the isLike
	# Symbols
	assert not isLike(Any, Nil)
	assert isLike(Nil, Any)
	assert isLike(Any, Any)
	assert isLike(Nil, Nil)
	# Cells
	assert isSubtype(Char, Cell)
	assert isLike(Char, Char)
	assert isLike(LongInteger, Float)
	assert isLike(Double, LongFloat)
	assert isLike(Double, Any)
	assert not isLike(Any, Double)
	assert not isLike(Nil, Double)
	assert not isLike(Double, Nil)
	# Arrays
	assert isSubtype(Array(Float), Array)
	assert isLike(Array(Float), Array(Any))
	assert isLike(Array(Any), Array(Any))
	assert isLike(Array(Nil), Array(Any))
	assert isLike(Array(Nil), Array(Nil))
	assert not isLike(Array(Any), Array(Nil))
	assert isLike(Array(Char), Array(Char))
	assert isLike(Array(LongInteger), Array(Float))
	# Sequences
	assert isSubtype(Sequence(), Sequence)
	assert isLike(Sequence(), Sequence())
	assert not isLike(Sequence(Any), Sequence(Float))
	assert isLike(Sequence(Float), Sequence(Any))
	assert isLike(Sequence(Float, Float), Sequence(Any, Float))
	assert isLike(Sequence(String, Float), Sequence(Any, Float))
	assert isLike(Sequence(Float, Float), Sequence(Float, Rest))
	assert isLike(Sequence(Float, Float, Any), Sequence(Float, Rest))
	# Maps
	assert isSubtype(Map(), Map)
	assert isLike(Map(), Map())
	assert isLike(Map(a=Nil), Map(a=Nil))
	assert not isLike(Map(a=Char), Map(a=Nil))
	assert  isLike(Map(b=String, a=Char), Map(a=Char, b=String))
	# Processes
	assert isSubtype(Process(Nothing, Nothing), Process)
	assert isSubtype(Function(Nothing, Nothing), Process)
	assert isLike(Process(Nothing, Nothing), Process(Nothing, Nothing))
	assert isLike(Process(Nil, Nothing), Process(Nil, Nothing))
	assert isLike(Process(Any, Any), Process(Any, Any))
	assert Process(Char, String).arguments().isLike(Char)
	assert Process(Char, Integer, String).arguments().isLike(Sequence(Char, Integer))
	assert Process(Char, String).result().isLike(String)
	p = Process()
	p.arguments((Any, Char))
	p.result(String)
	assert isLike(Process(Any, Char, String), p)
	assert p.arguments().isSameAs(Arguments(Any, Char))
	assert p.result().isSameAs(String)

	# TODO: Test processes arguments

	# FIXME: Function can take "Nothing" (Nil being a type for a singleton # value)
	assert isLike(Function(Float, Nil), Function(Any, Nil))

	# Now we test the isSubtype
	# Cells
	assert isSubtype(Char, Char)
	assert isSubtype(Integer, Char)
	assert not isSubtype(Char, Integer)
	assert isSubtype(Float, Char)
	assert isSubtype(Double, Char)
	assert not isSubtype(Char, Double)
	# Arrays
	assert isSubtype(Array(Any), Array)
	assert isSubtype(Array(Char), Array(Char))
	assert isSubtype(Array(Integer), Array(Char))
	assert isSubtype(Array(Float), Array(Char))
	assert isSubtype(Array(Double), Array(Char))
	assert not isSubtype(Array(Char), Array(Double))
	assert isSubtype(Array(Double), String)
	assert isSubtype(Array(Char), String)
	# Sequence
	assert isSubtype(Sequence(), Sequence)
	assert isSubtype(Sequence(), Sequence())
	assert isSubtype(Sequence(Any), Sequence(Any))
	assert isSubtype(Sequence(Char), Sequence(Char))
	assert isSubtype(Sequence(Any), Sequence())
	assert isSubtype(Sequence(Integer), Sequence(), )
	assert isSubtype(Sequence(Integer), Sequence(Char))
	assert isSubtype(Sequence(Float), Sequence(Char))
	assert isSubtype(Sequence(Float, Any), Sequence(Char))
	assert isSubtype(Sequence(Char, Rest), Sequence(Char))
	assert isSubtype(Sequence(Char, Integer), Sequence(Char, Rest))
	assert isSubtype(Sequence(Char, Rest), Sequence(Char, Integer))
	assert isSubtype(Sequence(Char, Rest), Sequence(Char, Integer, Char))

	# Python type classes
	assert isSubtype(Sequence(), Sequence)
	assert not isSubtype(Sequence(), Sequence(Char))
	assert isSubtype(Function(Nothing, Nothing), Process)
	assert isSubtype(Function(Char, Nothing), Process)

	a = Map()
	b = Map(a=Nil)
	assert isSubtype(b, a)
	c = Class(say=Function(String, Nil))
	d = Class(c, sayHello=Function(Nil,Nil))
	# NOTE: isSubtype(a,b) reads "is b a subtype of a"
	# and not "is a a subtype of b"
	assert isSubtype(d,c)
	assert not isSubtype(c,d)
	e = Class(d, sayHelloWorld=Function(Nil,Nil))
	assert isSubtype(e,d)
	assert isSubtype(e,c)

	# TODO: Do something for Array(Nothing)
# EOF
