#!/usr/bin/env python
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------

import sys, os, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../Sources")
from rugg.core import *

__doc__ = "Tests the producers."


DATA_LOCK = threading.Lock()
DATA = {}

def consumer_thread( name, producer ):
  print "Starting thread", name
  DATA_LOCK.acquire()
  DATA[name] = ""
  DATA_LOCK.release()
  # We enter the main consumption process
  while True:
    data, length = producer.consume(name)
    # The task is finished
    if data == None:
      # producer.consumerFinished(name)
      print "[%s] No more data available. Current data is %s" % (name, len(DATA[name]))
      return
    # Or we have read data
    else:
      assert len(data) == length
      print "[%s] read %s bytes..." % (name, length)
      DATA_LOCK.acquire()
      old_data = len(DATA[name])
      DATA[name] += data
      print "[%s] Merged data: %s" % (name, len(DATA[name]))
      assert old_data + length == len(DATA[name]), "%s != %s" % (old_data + length,  len(DATA[name]))
      DATA_LOCK.release()
      producer.consumerFinished(name)

if __name__ == "__main__":
  for threads_count in (1, 2, 3, 5, 10, 15):
    print "== TEST WITH %s THREADS" % (threads_count)
    NAMES = map(str, range(threads_count))
    def generate( size ):
      print "Testing with data size of", size
      producer = SharedProducer(size, producer=randomBinaryProducer)
      threads  = []
      # We create the threads and declare them
      for name in NAMES:
        threads.append(threading.Thread(target=consumer_thread, args=(name, producer)))
        producer.declareConsumer(name)
      # We start them only when they are all created
      for thread in threads: thread.start()
      # We wait for them to finish
      for thread in threads: thread.join()
      # We assert that the data is the same for all
      for name in NAMES:
        assert DATA[name] == DATA[NAMES[0]], name + " data differs"
      print "OK for size", size
    for s in (KB(10), KB(100), MB(1), MB(10)):
      print "SIZE", s
      print "================================================================"
      generate(s)
  print "OK"

# EOF

