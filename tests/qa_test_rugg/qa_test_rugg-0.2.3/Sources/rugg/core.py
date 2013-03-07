# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@xprima.com>
# License   : GNU Public License <http://www.gnu.org/licenses/gpl.html>
# Creation  : 03-Mar-2006
# Last mod  : 04-May-2006
# History   :
#             04-May-2006 - Added checks for out of date updatedb
#             03-Avr-2006 - Introduced the CachedProducer for speedups
#             23-Mar-2006 - Rewrote the SharedProducer class
#             22-Mar-2006 - Added read limit
#             21-Mar-2006 - Reworking of the operations implementation, and
#             moved them to the operations module.
#             20-Mar-2006 - Added locate interface, multi-threaded producer.
#             07-Mar-2006 - Got rid of words, replaced by urandom generator
#             06-Mar-2006 - Added limits, updated producers, added 'fill',
#             'ensure', 'blank' and 'generate' operations, and removed the
#             corresponding operations from the core classes.
#             03-Mar-2006 - Moved from `rugg.main` module
#
# -----------------------------------------------------------------------------

import os, sys, stat, sha, re, random, commands, threading

# The /dev/urandom random data generator
if not os.path.exists("/dev/urandom"):
  print "'/dev/urandom' is required by Rugg (for now)."""
  sys.exit(-1)

if commands.getstatusoutput("locate --version")[0] != 0:
  print "'locate' is required by Rugg. Please install it."""
  sys.exit(-1)

TEXT_SOURCES = []

# The regular expression for quantities
RE_SIZE = re.compile("^([0-9]+(\.[0-9]+)?)([kKmMGgtT]?[bBoO]|%)?$")

# ------------------------------------------------------------------------------
#
# Exceptions
#
# ------------------------------------------------------------------------------

class FileError(Exception):
  """Abstract class for file-related errors."""
  pass

class ReadError(FileError):
  """Indicates that a read operation did not work as expected."""
  pass

class WriteError(FileError):
  """Indicates that a write operation did not work as expected."""
  pass

class OperationalError(FileError):
  """Indicates than an operation (ensure, fill, etc) did not work as
  expected."""
  pass

# ------------------------------------------------------------------------------
#
# UNIT CONVERSION
#
# ------------------------------------------------------------------------------

def KB(size):
  """Returns the number of kilobytes in bytes"""
  return long(2 ** 10 * size)

def MB(size):
  """Returns the number of megabytes in bytes"""
  return long(2 ** 20  * size)

def GB(size):
  """Returns the number of gigabytes in bytes"""
  return long(2 ** 30  * size)

def TB(size):
  """Returns the number of terabytes in bytes"""
  return long(2 ** 40  * size)

# This table is used by the parseSize method to associate converting functions
# to quantity suffixes
UNITS = {"KB":KB, "MB":MB, "GB":GB, "TB":TB,"KO":KB, "MO":MB, "GO":GB, "TO":TB}
def parseSize(text):
  """Parses the given size as a string and returns the size in bytes"""
  match = RE_SIZE.match(text)
  if not match: return None
  size = float(match.group(1))
  unit = match.group(3)
  if unit == "%":
    size = size / 100.0
    return int(size * freespace())
  elif unit:
    unit = unit.upper()
    if unit == "B": return long(size)
    func = UNITS.get(unit)
    if not func: return None
    return func(size)
  else:
    return long(size)

# ------------------------------------------------------------------------------
#
# LIMITS
#
# ------------------------------------------------------------------------------

class Limits:
  """The Limits class defines limits that will constrain the operations defined
  in this modules. Limits allow to prevent the operation from overflowing or
  causing problem with the underlying operating systems. Limits are used to
  determine the maximum number of file descriptors, or the maximum length of
  data producer by a producer at a time.
  
  Attributes:
     MAX_FD             Maxium number of file descriptors openened at once
     MAX_PRODUCED_DATA  Maximum length of data produced by a producer
  """
  def __init__(self):
    self.MAX_FD            = 1000
    self.MAX_PRODUCED_DATA = MB(5)
    self.MAX_READ_DATA     = MB(5)
    self.CACHE_SIZE        = MB(10)

# Creates a new shared limits instance
LIMITS   = Limits()

# ------------------------------------------------------------------------------
#
# DATA PRODUCERS
#
# ------------------------------------------------------------------------------

# TODO: Implement proper producers
def randomNumberProducer( length ):
  """Returns a chunk of data of the given length, or of a length equal to
  LIMITS.MAX_PRODUCED_DATA if length is too big. The data and its lengths are
  returned anyway."""
  return randomBinaryProducer(length)

def randomWordsProducer( length ):
  """Returns a chunk of data of the given length, or of a length equal to
  LIMITS.MAX_PRODUCED_DATA if length is too big. The data and its lengths are
  returned anyway."""
  return randomBinaryProducer(length)

def randomBinaryProducer( length ):
  """Returns a chunk of data of the given length, or of a length equal to
  LIMITS.MAX_PRODUCED_DATA if length is too big. The data and its lengths are
  returned anyway."""
  res = ""
  if length < 0: length = LIMITS.MAX_PRODUCED_DATA
  length = min(length, LIMITS.MAX_PRODUCED_DATA)
  data = os.urandom(length)
  return data, length

def _initTextSources():
  global TEXT_SOURCES
  if not TEXT_SOURCES:
    TEXT_SOURCES = commands.getoutput("locate .txt .c .h .xml .html .css .py").split("\n")
  return

def _pickData( paths, length ):
  """Picks a file from the given list of paths, and returns at most the given
  length. If there was a problem with the given file (cannot be read, or does
  not exist), then None is returned."""
  def helper(paths=paths, length=length):
    i = random.randint(0,len(paths)-1)
    path = paths[i]
    if length < 0: length = LIMITS.MAX_PRODUCED_DATA
    length = min(length, LIMITS.MAX_PRODUCED_DATA)
    if os.path.exists(path) and os.path.isfile(path):
      try:
        # If there is any problem, we skip
        f = file(path, 'r')
        d = f.read(length)
        f.close()
      except:
        d = None
      if d:
        return d, len(d)
      else:
        return None
    else:
      return None
  tries = 0
  while tries < 100:
    res = helper()
    if res != None:
      return res
    else:
      tries += 1
  raise OperationalError("Your locate database seems out of date. Run `updatedb`")

def randomTextProducer( length ):
  """Returns a chunk of data of the given length, or of a length equal to
  LIMITS.MAX_PRODUCED_DATA if length is too big. The data and its lengths are
  returned anyway."""
  _initTextSources()
  return _pickData(TEXT_SOURCES, length)

def blankProducer( length ):
  """Returns a chunk of data of the given length, or of a length equal to
  LIMITS.MAX_PRODUCED_DATA if length is too big. The data and its lengths are
  returned anyway."""
  if length < 0: length = LIMITS.MAX_PRODUCED_DATA
  length = min(length, LIMITS.MAX_PRODUCED_DATA)
  return " " * length, length

# ------------------------------------------------------------------------------
#
# PRODUCERS CLASSES
#
# ------------------------------------------------------------------------------

class CachedProducer:
  """A cached producer generates a certain amount of data and picks its data
  from the cache. This allows to speed up the throughput and do actual
  benchmarking.
  
  To generate a cached producer simply do CachedProducer(randomTextProducer), or
  with whatever producer you prefer.
  """
  def __init__(self, producer=randomBinaryProducer):
    self._data = ""
    # We fill the cache
    while len(self._data) < LIMITS.CACHE_SIZE:
      d, l = randomBinaryProducer(LIMITS.CACHE_SIZE - len(self._data))
      self._data += d
    # We are now ready

  def __call__( self, length ):
    length = min(length, len(self._data))
    return self._data[:length], length



class SharedProducer:
  """This class allows to wrap a producer so that the same data can be consumed
  by a given number of threds. This is vital to the 'fill same' operation in
  multi-threaded contexts."""

  def __init__(self, totalSize, bufferSize=MB(1), producer=randomBinaryProducer,
  expectedConsumers=-1):
    assert totalSize > 0
    assert bufferSize > 0
    # Attributes
    self.expectedConsumers = expectedConsumers
    self.consumers         = {}
    self.producer          = producer
    self.totalSize         = totalSize
    self.bufferSize        = min(totalSize, bufferSize)
    self.writtenSize       = 0
    # Internal attributes
    self._data             = None
    self._dataLenght       = 0
    self._iteration        = -1
    self._consumed         = 0
    # State
    self._lock             = threading.Lock()
    self._condition        = threading.Condition()
    self._enoughConsumersDeclared = threading.Event()
    self._enoughConsumersDeclared.clear()

  def declareConsumer( self, consumer ):
    """This has to be called at the beginning by each consumer."""
    self.consumers[consumer] = 0
    assert self.expectedConsumers == -1 or len(self.consumers) <= self.expectedConsumers, "Too many consumers registerd"
    # We only start when the expected consumer count is met
    if len(self.consumers) == self.expectedConsumers or self.expectedConsumers:
      if self._iteration == -1:
        self._condition.acquire()
        self._iterate()
        self._condition.release()

  def cleanConsumer( self, consumer ):
    """Calles at the very end, when the consumer does not which to consume data
    anymore."""
    del self.consumers[consumer]
    if self.expectedConsumers != -1 and len(self.consumers) < self.expectedConsumers:
      self._enoughConsumersDeclared.clear()

  def reset( self ):
    self.writtenSize = None
    self._iteration  = -1
    self._consumed   = 0
    self._data       = None
    self._dataLength = None

  def consumerFinished( self, consumer ):
    """This MUST be called by the consumer after each time it properly consumed
    data. This SHOULD NOT be called when the data returned is (None, 0)."""
    # This must be called for each consumer in the current iteration
    assert self.consumers[consumer] == self._iteration
    self._condition.acquire()
    self.consumers[consumer] += 1
    self._consumed           += 1
    # When every consumer has consumed, we iterate
    if self._consumed == len(self.consumers):
      self._iterate()
    self._condition.release()

  def isConsumerDeclared( self, consumer ):
    return self.consumers.get(consumer) != None

  def _iterate( self ):
    # Can we generate more data ?
    if self.writtenSize < self.totalSize:
      self._data       = None
      self._consumed   = 0
      self._iteration += 1
      self._data, self._dataLength = self.producer(min(self.totalSize - self.writtenSize, self.bufferSize))
      self.writtenSize += self._dataLength
      assert self._data != None
      assert self._dataLength > 0, "??? %s, %s = %s" % (self.writtenSize, self.totalSize, self._dataLength)
      assert self.writtenSize <= self.totalSize, "Produced too much data %s > %s" % (self.writtenSize, self.totalSize)
    else:
      self._data = None
      self._dataLength = 0
      self._iteration += 1
    # We notify the consumers that we have data available
    self._condition.notifyAll()

  def consume( self, consumer ):
    """This is a (blocking) operation that produces the data. When all the data
    is produced this returns None"""
    # Consumption can only start when the DECLARATION phase is finished
    self._condition.acquire()
    assert self._iteration <= self.consumers[consumer]
    while not self.consumers[consumer] == self._iteration:
      self._condition.wait()
    self._condition.release()
    return self._data, self._dataLength

# ------------------------------------------------------------------------------
#
# GENERIC OPERATIONS
#
# ------------------------------------------------------------------------------

def rseek(files, offset):
  if type(files) not in (tuple,list): files = (files,)
  for f in files:f.rseek(offset)

def wseek(files, offset):
  if type(files) not in (tuple,list): files = (files,)
  for f in files:f.wseek(offset)

def seek(files, offset):
  if type(files) not in (tuple,list): files = (files,)
  for f in files:f.seek(offset)

def freespace( path="." ):
  t = os.popen("df -k '%s'" % (path)).read()
  t = tuple(f.strip() for f in t.split("\n")[-2].split(" ") if f.strip())
  return KB(int(t[3]))

# ------------------------------------------------------------------------------
#
# FILE OBJECT
#
# ------------------------------------------------------------------------------

_CLASSES_COUNT = {}

#TODO: Asserts that operations do not exceed the bounds
class File:
  """Files objects are a simple abstraction that easily allow to read, write,
  seek and unlink files. These are the objects used to access the filesystem and
  to harness the hard drives."""

  def __init__( self, path, sizeLimit=-1, baseOffset=0, ensureNew=True,
  logger=None ):
    """Creates a new test file with the given path. The file MUST NOT EXIST, and
    it will be created, write and read file descriptors will then be opened on
    that file."""
    class_name = self.__class__.__name__
    count = _CLASSES_COUNT.setdefault(class_name, 1)
    self.shortname       = "%s:%04d" % (class_name, count) 
    _CLASSES_COUNT[class_name] = count + 1
    self._logger         = logger
    self._path           = os.path.abspath(path)
    self._writefd        = None
    self._readfd         = None
    self._sizeLimit      = sizeLimit
    self._baseOffset     = baseOffset
    self._currentROffset = 0
    self._currentWOffset = 0
    # We check if the size limit exceeds the available free space
    if sizeLimit != -1:
      free_space = freespace()
      if freespace() < sizeLimit:
        raise FileError("Not enough free space for filled up file : %s, required %s" % (free_space, sizeLimit))
    # If the file already exist and that we have "ensureNew", we recreate it
    if ensureNew and os.path.exists(self._path):
      os.unlink(self._path)
      f = open(self._path,"w") ; f.close()
    self._createDescriptors()
    # We do a seek 0 to jump to the proper location, in case the baseOffset was
    # set.
    self.seek(0)

  def __str__( self ):
    """Gives a string representation of this file."""
    res  = "%s at %s\n" % ( self.__class__.__name__, self._path)
    res += " rfd  : %s:%sbytes\n" % ( self._readfd,  self._currentROffset)
    res += " wfd  : %s:%sbytes\n" % ( self._writefd, self._currentWOffset)
    res += " size : %s <= %s, %s free\n" % ( self.size(), self.sizeLimit(), self.availableSpace())
    return res

  def _createDescriptors( self ):
    """This method is invoked by the constructor and creates the file
    descriptors (by default, one read and one write for the given path). This
    should be overriden if different behaviours are expected."""
    # TODO: Maybe used th O_SYNC flag too.. have to dig out what it is exactly
    self._writefd = os.open(self.path(), os.O_RDWR|os.O_CREAT|os.O_SYNC)
    self._readfd  = self._writefd

  def unlink( self ):
    """Unlinks this file. This closes the opened file descriptors and deletes
    the files from the filesystem."""
    if self._readfd: os.close(self._readfd)
    if self._writefd and self._writefd!=self._readfd: os.close(self._writefd)
    self._readfd = None
    self._writefd = None
    if os.path.exists(self._path):
      os.unlink(self._path)

  def seek( self, offset ):
    """Moves both read and write offsets to the given offset."""
    self.rseek(offset)
    self.wseek(offset)

  def rseek( self, offset ):
    """Moves the read fd to the given offset."""
    assert self._readfd
    assert self.sizeLimit() == -1 or offset <= self.sizeLimit(), "Offset exceeded size limit %s > %s in %s" % (offset, self.sizeLimit(), self)
    self._currentROffset = offset
    return os.lseek(self._readfd, self._baseOffset + self._currentROffset, 0)

  def wseek( self, offset ):
    """Moves the write fd to the given offset."""
    assert self._writefd
    assert self.sizeLimit() == -1 or offset <= self.sizeLimit(), "Offset exceeded size limit %s > %s in %s" % (offset, self.sizeLimit(), self)
    self._currentWOffset = offset
    return os.lseek(self._writefd, self._baseOffset + self._currentWOffset, 0)

  def rtell( self ):
    return os.lseek(self._readfd, 0, 1)

  def wtell( self ):
    return os.lseek(self._writefd, 0, 1)

  def flush( self ):
    """Flushes the buffers."""
    if self._writefd: os.fsync(self._writefd)

  def read( self, length=-1 ):
    """Reads a segment of data of the given length and returns it. If an empty
    string is returned, then no value was read."""
    if length == -1: length = self.size()
    assert self._readfd
    # We make sure that we are positioned at the expected offset (this may slow
    # down the process, but it si mandatory)
    self.rseek(self._currentROffset)
    if self.size() != -1:
      length = min(length, self.sizeLimit() - self._currentROffset)
    length = min(length, LIMITS.MAX_READ_DATA)
    data = os.read( self._readfd, length)
    self._currentROffset += len(data)
    return data

  def produce( self, length=-1 ):
    """This method can be used as a producer, and will return the content of
    this file from the current reading position."""
    data = self.read(length)
    return data, len(data)

  def write( self, data ):
    """Writes the given data to this file. Returns the actual number of written
    bytes."""
    assert self._writefd
    assert len(data) > 0, repr(data)
    # We make sure that we are positioned at the expected offset (this may slow
    # down the process, but it si mandatory)
    self.wseek(self._currentWOffset)
    length = len(data)
    if self.sizeLimit() != -1:
      length = min(length, self.sizeLimit() - self._currentWOffset)
    res = os.write(self._writefd, data[:length])
    if not length == res:
      raise WriteError("Tried to write %s bytes of data, only %s were written."
      % (length, res), "in file: " + str(self))
    self._currentWOffset += res
    return res

  def size( self ):
    """Returns the current size of this file, in bytes."""
    # We flush the read fd, as there may still be some uncommited data, and then
    # the returned size will be smaller than expected
    self.flush()
    stat_info = os.stat(self._path)
    return stat_info[stat.ST_SIZE]

  def path( self ):
    """Returns the path for this File."""
    return self._path

  def sizeLimit( self ):
    """Returns the size limit for this file. -1 means that the file has no size
    limit, otherwise file size limit is expressed in bytes."""
    return self._sizeLimit

  def canWrite( self ):
    """Returns the number of bytes that can be written until the size limit is
    reached. This returns -1 if there is no limit set."""
    if self.sizeLimit() != -1:
      return self.sizeLimit() - self._currentWOffset
    else:
      return -1

  def limitSize( self, sizeLimit ):
    """Sets a limit to this file size."""
    self._sizeLimit = sizeLimit

  def availableSpace( self ):
    """Returns the available space (in bytes) for writing this file."""
    res = filter(lambda x:x.strip(), commands.getoutput("df -kP /home").split("\n")[-1].split(" "))[3]
    return KB(long(res))
    
  def data( self ):
    """Returns the content of this file as data. The current read offset is
    preserved"""
    prev_offset = self._currentROffset
    self.rseek(0)
    data = self.read()
    self.rseek(prev_offset)
    return data

  def sig( self ):
    """Returns the SHA-1 signature for this file."""
    return sha.new(self.data()).hexdigest()

# ------------------------------------------------------------------------------
#
# ZONES
#
# ------------------------------------------------------------------------------

def generate_path( prefix="zone", suffix=".data", parent="" ):
  counter = 0
  if parent and parent[-1]!="/": parent += "/"
  while os.path.exists( parent + prefix + "_" + str(counter) + suffix ):
    counter += 1
  return parent + prefix + "_" + str(counter) + suffix

class Zone(File):
  """A Zone is a specific file with a specific given size which can be divided
  into multiple SubZones. This allows to tests specific locations on the
  filesystem by creating 'virtual files' within one big file."""

  def __init__( self, path=None, size=0, **kwargs ):
    """Creates a new zone at the given path with the given size. The zone is
    not filled with any data."""
    if not path: path = generate_path()
    File.__init__(self, path, size, **kwargs)
    self._subzones = []

  def subdivide( self, number ):
    """Divides the zones into the given number of subzones. Starting from that
    moment, and until join is invoked, all operations will be made on all
    subzones. An array of SubZones representing the subzones themselves is
    given, and can be manipulated as regular files."""
    self.flush()
    assert len(self._subzones) == 0
    file_size = self.sizeLimit() / number
    offset    = 0
    while number > 0:
      sub_zone = SubZone(self, offset, file_size)
      self._subzones.append(sub_zone)
      offset += file_size
      number -= 1
    return tuple(self._subzones)

  def subzone( self, baseOffset, length ):
    """Creates a subzone with the given base offset and the given length. There
    is no checking for wether the subzone overlaps with an existing one, so you
    should take care of that."""
    assert baseOffset + length <= self.sizeLimit
    sub_zone = SubZone(self, baseOffset, length)
    self._subzones.append(sub_zone)
    return sub_zone

  def subzones( self ):
    """Returns the subzones that were created when this zone was divided, if it
    was divided."""
    return tuple(self._subzones)

  def join( self ):
    """This is the opposite of divide: it joins every subzone together, so that
    this zone is a single zone."""
    self.flush()
    while self._subzones:
      sub_zone = self._subzones.pop()
      sub_zone.unlink()

  def size( self ):
    """Returns the current size of this file, in bytes."""
    for sub_zone in self._subzones: sub_zone.flush()
    return File.size(self)

# ------------------------------------------------------------------------------
#
# ZONEFILES AKA SUBZONES
#
# ------------------------------------------------------------------------------

class SubZone(File):
  """A Zone file is a file that leaves within a zone. It has the same interface
  as the File object."""

  def __init__( self, zone, startOffset, size, **kwargs ):
    self._zone         = zone
    self._zoneSize     = size
    File.__init__(self, zone.path(), size, baseOffset=startOffset,
    ensureNew=False, **kwargs)

  def unlink( self ):
    """Unlinking Zone files has no side-effect, as the file descriptors are
    borrowed from the parent zone """
    if self._readfd:  os.close(self._readfd)
    if self._writefd != self._readfd: os.close(self._writefd)
    self._zone = None

  def size( self ):
    """Returns the current size of this file, in bytes."""
    return self._zoneSize

  def zone( self ):
    """Returns the zone to which this subzone comes."""
    return self._zone

# EOF
