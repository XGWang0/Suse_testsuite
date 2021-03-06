vim: set sts=2 sw=2 et

create with compression method lh7
------

  $ . $TESTDIR/functions

  $ rm -f archive_file.lzh

  $ mydd count=96 of=fileA
  96+0 records in
  96+0 records out

  $ mydd count=192 of=fileB
  192+0 records in
  192+0 records out

  $ mydd count=290 of=fileC
  290+0 records in
  290+0 records out

  $ mkdir directoryA directoryB

  $ lha -co7 archive_file.lzh fileA directoryA fileB directoryB
  
  directoryA/\t- Frozen(0%) (esc)
  
  directoryB/\t- Frozen(0%) (esc)
  
  fileA\t- Freezing :  . (esc)
  fileA\t- Freezing :  o (esc)
  fileA\t- Frozen(100%) (esc)
  
  fileB\t- Freezing :  .. (esc)
  fileB\t- Freezing :  oo (esc)
  fileB\t- Frozen(100%) (esc)

