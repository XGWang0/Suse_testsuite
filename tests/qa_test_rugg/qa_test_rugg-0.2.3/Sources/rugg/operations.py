# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@xprima.com>
# License   : GNU Public License <http://www.gnu.org/licenses/gpl.html>
# Creation  : 16-Mar-2006
# Last mod  : 28-Avr-2006
# History   :
#             28-Avr-2006 - Added error handling in env
#             03-Avr-2006 - Renamed @dipatch to @method. Added the 'time'
#             method, extended the 'fill' method. Added a preliminary benchmark
#             operation.
#             24-Mar-2006 - Added the 'do' operation
#             21-Mar-2006 - Moved operations from the core, implemented
#             contexts. Fill same implementation.
#             20-Mar-2006 - Added fill with type, and ensure methods.
#             17-Mar-2006 - Bugfixes and additions
#             16-Mar-2006 - First implementation (2 time shorter than before)
# -----------------------------------------------------------------------------

import types, os, threading, time
from rugg.typesystem import *
from rugg import typecast
from rugg import core, logger

__doc__ = """\
The operations module defines an Environment class that contains all the
operations. It is automatically instanciated by a program (in the language
module).

What is interesting is that the Environment allows to very easily bind
operations between Rugg and Python. You simply have to decorate an Environment
method with the @method decorator, which will explicitely indicate the method
signatures (we take advantage of Python flexible typing).
"""
# ------------------------------------------------------------------------------
#
# OPERATIONS
#
# ------------------------------------------------------------------------------

def method(*types):
  """Decorates the given function by associating to it a dispatching type."""
  def decorator(f):
    if "_signatures" not in f.__dict__.keys(): f._signatures = []
    f._signatures.extend(types)
    return f
  return decorator

class Environment:
  """The operations environment is a class that encapsulates all operations defined in the
  language. It offers a simple framework to implement what is defined in the
  language."""

  def __init__( self, program=None ):
    self._methods     = {}
    self._contexts    = [{}]
    self._time        = None
    self._duration    = None
    self._errors      = 0
    self._contextLock = threading.Lock()
    self.program      = program

  # LOGGING
  # ___________________________________________________________________________

  def indent( self, text, length, firstline ):
    text = str(text)
    r = ""
    for line in text.split("\n"):
      if firstline: r += " " * length
      else: firstline = True
      r += line + "\n"
    if r and r[-1] == "\n": r=r[:-1]
    return r

  def log( self, message ):
    print "%s: %s" % (logger.format("%10s" % (threading.currentThread().getName()),
    logger.CYAN), self.indent(message, 12, False))

  def error( self, message ):
    print "%s! %s" % (logger.format("%10s" % (threading.currentThread().getName()),
    logger.RED), self.indent(message, 12, False))
    self._errors += 1

  # BOILER PLATE
  # ___________________________________________________________________________

  def register( self ):
    """Should be called after the instanciation. Will register all functions
    that have been decorated with @method."""
    self._methods = {}
    for slot in dir(self):
      value = getattr(self,slot)
      if type(value) == types.MethodType and "_signatures" in \
      value.__dict__.keys():
        v = slot.find("_")
        method_name = slot
        if v != -1: method_name = slot[:v]
        methods = self._methods.setdefault(method_name, [])
        #DEBUG
        #print "@" + slot + ":"
        #for s in value._signatures:
        #  print "  ", s.asString()
        #print
        methods.append((value._signatures, value))

  def listOperations( self ):
    """Returns a list of couples ("operation name", "method")."""
    r = []
    for name, method in self._methods.items():
      r.append((name, method))
    return r

  def _dispatch( self, operation, argSignature ):
    implementations = self._methods.get(operation)
    if not implementations: raise UndefinedOperation(operation)
    # We iterate on all the operation implementations
    for processes, implementation in implementations:
      # Each implementation can respond to more than one signature
      for process in processes:
        # print process
        # print "isLike", operation," sig:", process.arguments(), "args:", argSignature, argSignature.isLike(process.arguments())
        if argSignature.isLike(process.arguments()):
          return implementation, process.result()
    # If we arrived there, we the given arguments do not match
    raise OperationDoesNotRespond("%s %s" % (operation, argSignature.asString()))

  def returnType( self, operation, argsignatures ):
    return self._dispatch(operation, argsignatures)[1]

  def invoke( self, operation, argsignatures, arguments ):
    """Invokes the given operation with the given arguments. The arguments must
    be actual ProgramModel Values, and must be able to return a type."""
    #print operation, argsignatures, self._dispatch(operation, argsignatures)[0], arguments
    return apply(self._dispatch(operation, argsignatures)[0], arguments)

  # RUNTIME EVENTS
  # ___________________________________________________________________________

  def start( self ):
    """Program started."""
    self._time = time.time()

  def startContext( self, **kwargs ):
    """Starts a new subcontext in the environment. A context can be used by the
    operations to save run-time state data."""
    self._contexts.append({})
    for key, value in kwargs.items():
      self._contexts[-1][key] = value
  
  def endContext( self ):
    """Ends the context that was previously created by the 'startContext'"""
    self._contexts.pop()

  def context( self, name="", **kwargs ):
    """Queries the given element of the current context or adds the given
    key/values to the current context."""
    if kwargs:
      for key, value in kwargs.items():
        self._contexts[-1][key] = value
    else:
      res = self._contexts[-1].get(name)
      return res

  # OPERATIONS IMPLEMENTATION
  # ___________________________________________________________________________

  @method( Process(Quantity, Zone))
  def zone( self, quantity ):
    zone = self.program.createZone(size=quantity)
    self.log("Created %sb zone at '%s' (%s)" % (quantity, os.path.basename(zone.path()), zone.shortname))
    return zone
  
  @method( Process(Array(Quantity), Array(Zone)))
  def zone_array( self, quantities ):
    res = []
    self.log("Creating %s zones..." % (quantity))
    for quantity in quantities: self.zone(quantities)
    return res

  @method(Process(Zone, Quantity, Array(Zone)))
  def subdivide( self, zone, quantity ):
    self.log("Subdividing %s in %s..." % (zone.shortname, quantity))
    subzones = zone.subdivide(quantity)
    return subzones

  @method(Process(Quantity, Zone, Array(Zone)))
  def subdivide_alt( self, quantity, zone):
    return self.subdivide(zone, quantity)

  # GENERATE ===================================================================

  @method(
    Process(Zone, Zone),
    Process(Zone, Quantity, Zone),
    Process(Zone, Quantity, Quantity, Zone),
  )
  def generate( self, f , length=-1, blocksize=core.LIMITS.MAX_PRODUCED_DATA,
    producer=core.randomTextProducer ):
    # We check that the parameters are consistent
    if length < 0:
      raise core.OperationalError("Generated data length should be >= 0")
    if f.sizeLimit() != -1 and length > f.canWrite():
      raise core.OperationalError("Given length is too important. This file has " +
      "%s until limit, while requesting to generate %s." % (f.canWrite(), length))
     # We are now ready to fill the data with the given producer
    total_written = 0
    while total_written < length:
      # We generate a chunk of data
      data, data_len = producer(length - total_written)
      # And write it to the given files
      written = f.write(data)
      if written == 0: break
      # We add the number of bytes written to the total number of bytes written
      total_written += written
    # Eventually ensures that the expected number of bytes was written
    if total_written != length:
      raise core.OperationalError("Expected to write %sb on %s, but %s written." %
      (length, self.shortname, total_written))
    return f

  # FILL =======================================================================

  @method(Process(Zone, Zone))
  def fill( self, f, length=None, blocksize=core.LIMITS.MAX_PRODUCED_DATA,
    producer=core.randomTextProducer, log=True):
    # We check that the input is consistent
    size = length
    if size in (None, -1):  size = f.sizeLimit()
    elif f.sizeLimit()!=-1: size = min(size, f.size())
    if size == -1:
      raise core.OperationalError("At least one given file must have a size limit.")
    # We log the operation
    if log: self.log("Filling %s with %sb of data..." % (f.shortname, size))
    # Seeks writing to 0 
    f.wseek(0)
    return self.generate(f, size, blocksize, producer)

  def fill_argstokwargs( self, args ):
    """Utility function that converts the given string arguments as a dict that
    can be used as kwargs to the core.fill operation."""
    kwargs = {}
    fast     = False
    producer = None
    for arg in args:
      if arg.lower() == "same": kwargs["method"]="same"
      elif arg.lower() == "text": producer=core.randomTextProducer
      elif arg.lower() == "binary": producer=core.randomBinaryProducer
      elif arg.lower() == "fast": fast=True
      else: raise RuntimeError("Unknown fill argument: '%s'" % (arg))
    if fast and producer: producer = core.CachedProducer(producer)
    kwargs["producer"] = producer
    return kwargs

  @method(
    Process(String, Zone, Zone),
    Process(String, String, Zone, Zone),
    Process(String, String, String, Zone, Zone),
  )
  def fill_typeWithZones(self, *args, **pkwargs):
    # TODO: Detect wether producer or method
    kwargs = self.fill_argstokwargs(args[:-1])
    for key, value in pkwargs.items(): kwargs[key] = value
    zone  = args[-1]
    producer = kwargs.get("producer") or core.randomTextProducer
    # Are we writing the same data ?
    # NOTE: The "fill same" operation is special because it has to carry state
    # between the different successive invocations in the current context. Thus,
    # this implementation uses the context to store the necessary information.
    if kwargs.get("method") == "same":
      # If so, are we in parallel mode ?
      # The implementation of the parallel mode uses the core.SharedProducer
      # which is useful for distributing the same data to multiple threads
      if self.context("mode") == "parallel":
        # We get the shared producer, or create it
        # We ensure that this section is an atomic section, so that we have
        # onlye ONE producer created.
        self._contextLock.acquire()
        shared_producer = self.context("sharedproducer")
        if shared_producer == None:
          shared_producer = core.SharedProducer(zone.sizeLimit(),
          producer=producer, expectedConsumers = len(self.context("elements")))
          self.context(sharedproducer=shared_producer)
        self._contextLock.release()
        # We register the zone as a consumer if it was not already
        if not shared_producer.isConsumerDeclared(zone.shortname):
          shared_producer.declareConsumer(zone.shortname)
        # Now we consume
        self.log("Filling %s with %sb of same data..." % (zone.shortname, shared_producer.totalSize))
        while True:
          data, length = shared_producer.consume(zone.shortname)
          if length > 0:
            zone.write(data)
            shared_producer.consumerFinished(zone.shortname)
          else:
            break
        # And eventually return the zone
        return zone
      # We are in sequential mode.
      # The strategy here is quite simple : we fill the first zone entirely,
      # then we simply copy its content to the other zones
      elif self.context("mode") == "sequential":
        if self.context("firstzone") == None:
          self.context(firstzone=zone)
          self.fill(zone, producer=producer)
        else:
          first_zone = self.context("firstzone")
          first_zone.rseek(0) ; zone.wseek(0)
          self.fill(zone, producer=first_zone.produce)
        return zone
      else:
        # FIXME: Maybe we could generalize this and make it apply to zones or
        # regular files.
        raise core.OperationalError("fill same can only be used with iterations/applications")
    # When we are not in 'fill same' mode, things are way simpler.
    else:
      self.fill(zone, producer=producer)
      return zone

  # BLANK =======================================================================

  @method(
    Process(Zone, Zone),
    Process(Array(Zone), Array(Zone)))
  def blank(self,zone):
    if type(zone) in (tuple, list):
      for z in zone:
        self.blank(z)
    else:
      self.log("Blanking %sb in zone %s." % (zone.size() or zone.sizeLimit(), zone.shortname))
      self.fill(zone, producer=core.blankProducer, log=False)
    return zone

  # ENSURE ======================================================================

  def ensureSame( self, files, opposite=False, blocksize=core.LIMITS.MAX_READ_DATA ):
    if not type(files) in (tuple, list): files = [files]
    if len(files) < 2:
      self.error("Ensuring 'same' or 'different' requires a set of zones.")
      return False, ""
    if not opposite:
      size = files[0].size()
      for f in files:
        if not f.size() == size:
          return False, "File size is %s, expected %s:\n%s" % (f.size(), size, f)
      for f in files: f.rseek(0) ; f.flush()
    # And we start reading the data
    data = True
    while data:
      data = new_data = None
      for f in files:
        new_data = f.read(blocksize)
        if data != None:
          # Here, we reached the end of of the file 
          if new_data == "": continue
          if not opposite and new_data != data or \
          opposite and new_data == data:
            return False, "%s has not the expected content." % (f.shortname)
        elif data == None:
          data = new_data 
    # TODO: Maybe restore the offsets at the positions they were
    return True, ""

  def ensureBlank( self, files, opposite=False, blocksize=core.LIMITS.MAX_READ_DATA ):
    if not type(files) in (tuple, list): files = [files]
    for f in files: f.rseek(0) ; f.flush()
    # And we start reading the data
    data = True
    while data:
      data = new_data = None
      for f in files:
        new_data = f.read(blocksize)
        if new_data != None:
          # Here, we reached the end of of the file 
          if new_data == "": continue
          if not opposite and new_data.strip() or \
                 opposite and not new_data.strip():
            return False, "%s has not the expected content." % (f.shortname)
        elif data == None:
          data = new_data 
    # TODO: Maybe restore the offsets at the positions they were
    return True, ""

  @method(
    Process(String, Zone, Zone),
    Process(String, String, Zone, Zone),
    Process(String, Array(Zone), Array(Zone)),
    Process(String, String, Array(Zone), Array(Zone)),
  )
  def ensure(self, *args ):
    zone = args[-1]
    args = args[:-1]
    # Here we test if we want the same, blank or different
    if len(args) == 1:
      what = args[0]
      mod  = ""
    else:
      what = args[1]
      mod  = args[0]
    what = what.lower()
    mod  = mod.lower()
    if mod not in ("not", ""): raise RuntimeError("Expected 'not' or nothing, got '%s'" % (mod))
    if what not in ("same", "different", "blank"): raise RuntimeError("Expected 'same', 'different' or 'blank', got '%s'" % (what))
    if what == "different" and mod == "not": what = "same" ; mod = ""
    if what == "different" and mod == "":    what = "same" ; mod = "not"
    # We run the stuff
    if type(zone) in (tuple, list):
      self.log("Ensuring that (%s) zones are %s %s" % (len(zone), mod, what))
    else:
      self.log("Ensuring that %s zone is %s %s" % (zone.shortname, mod, what))
    if what == "blank":
      result, value = self.ensureBlank( zone, opposite = mod == "not" )
    else:
      result, value = self.ensureSame( zone, opposite = mod == "not" )
    if not result:
      raise RuntimeError("Assertion failed: " + value)
    return zone

  # UNLINK ======================================================================

  @method(
    Process(Zone, Nothing),
    Process(Array(Zone), Nothing))
  def unlink(self,zone):
    if type(zone) in (list,tuple):
      for z in zone: self.unlink(z)
    else:
      self.log("Unlinking %s at '%s'" % (zone.shortname, zone.path()))
      zone.unlink()

  # SIG =========================================================================

  @method(
    Process(Zone, Zone),
    Process(Array(Zone), Array(Zone))
  )
  def sig(self,zone):
    if type(zone) in (list,tuple):
      for z in zone: self.sig(z)
    else:
      self.log("%s signature : %s" % (zone.shortname, zone.sig()))
    return zone

  # BENCH =========================================================================

  @method(
    Process(Nothing, Nothing),
    Process(Zone, Zone),
    Process(Array(Zone), Array(Zone)),
  )
  def time( self, something = Nothing ):
    t = time.time()
    self.log("operation took %.3fs." % (t - self._time))
    self._duration = t - self._time
    self._time = t
    return something

  @method(
    Process(Nothing, Nothing),
    Process(Zone, Zone),
    Process(Array(Zone), Array(Zone)),
  )
  def benchmark( self, something = Nothing ):
    # Creation of zones
    self.log("Rugg Benchmarking Suite")
    self.log("=======================")
    self.log("")
    results = []
    start   = time.time()
    sizes   = (core.MB(1), core.MB(5), core.MB(10), core.MB(20), core.MB(30),
    core.MB(40), core.MB(50), core.MB(100))
    # We create 1 + 5 + 10 + 20 + 30 + 40 + 50 =  256Mb
    producer = core.CachedProducer(core.randomBinaryProducer)
    for i in sizes:
      zone = self.zone(i)
      self.fill(zone, producer=producer )
      self.unlink(zone)
    duration = time.time() - start
    self.log("==> Step 1.0: Zone creation in %.3f (%.2fMb/s)" % (duration, 256/duration))
    self.log("")
    results.append(("1.0", duration))
    # Step 2: producers benchmark
    def step_2(producer):
      t = time.time()
      for i in sizes:
        zone = self.zone(i) ; self.fill(zone, producer=producer) ; self.unlink(zone)
      return time.time() - t
    duration = step_2(core.blankProducer)
    self.log("==> Step 2.0: Blank producer in %.3f (%.2fMb/s)" %
    (duration, 256/duration)) 
    self.log("")
    results.append(("2.0", duration))
    duration = step_2(core.randomTextProducer)
    self.log("==> Step 2.1: Random text producer in %.3f (%.2fMb/s)" %
    (duration, 256/duration)) 
    self.log("")
    results.append(("2.1", duration))
    duration = step_2(core.randomBinaryProducer)
    self.log("==> Step 2.2: Random binary producer in %.3f (%.2fMb/s)" %
    (duration, 256/duration)) 
    self.log("")
    results.append(("2.2", duration))
    duration = step_2(core.CachedProducer(core.randomTextProducer))
    self.log("==> Step 2.3: Cached random text producer in %.3f (%.2fMb/s)" %
    (duration, 256/duration)) 
    self.log("")
    results.append(("2.3", duration))
    duration = step_2(core.CachedProducer(core.randomBinaryProducer))
    self.log("==> Step 2.4: Cached random binary producer in %.3f (%.2fMb/s)" %
    (duration, 256/duration)) 
    self.log("")
    results.append(("2.4", duration))
    # We sum up the benchmark
    total = 0
    for test, duration in results:
      total += duration
      self.log("%s\t:\t%.3f\t%.3fMb/s" % (test, duration, 256 / duration))
    self.log("--")
    self.log("total\t%.3f (mean %.3fMb/s)" % (total, ( 256.0 * len(results)) / total))
    return something

  # JOIN ========================================================================

  @method(
    Process(Zone, Zone),
    Process(Array(Zone), Zone))
  def join( self, zones ):
    if type(zones) in (list,tuple):
      parent = None
      for z in zones:
        # FIXME: Throw runtime error
        if not parent: parent = z.zone()
        else: assert z.zone() == parent, "Zones do not match %s != %s" % (z.zone(), parent)
      parent.join()
      return parent
    else:
      zones.join()
      return zones

# EOF
