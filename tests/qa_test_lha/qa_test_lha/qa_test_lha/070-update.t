vim: set sts=2 sw=2 et

update archive
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

  $ mydd count=48 of=directoryA/fileAA
  48+0 records in
  48+0 records out

  $ mydd count=24 of=directoryB/fileBA
  24+0 records in
  24+0 records out

  $ touch -d @0 fileA fileB directoryA directoryA/fileAA directoryB directoryB/fileBA fileC

  $ lha c archive_file.lzh fileA directoryA fileB directoryB
  
  directoryA/\t- Frozen(0%) (esc)
  
  directoryA/fileAA\t- Freezing :  ... (esc)
  directoryA/fileAA\t- Freezing :  ooo (esc)
  directoryA/fileAA\t- Frozen(100%) (esc)
  
  directoryB/\t- Frozen(0%) (esc)
  
  directoryB/fileBA\t- Freezing :  .. (esc)
  directoryB/fileBA\t- Freezing :  oo (esc)
  directoryB/fileBA\t- Frozen(100%) (esc)
  
  fileA\t- Freezing :  ...... (esc)
  fileA\t- Freezing :  oooooo (esc)
  fileA\t- Frozen(100%) (esc)
  
  fileB\t- Freezing :  ............ (esc)
  fileB\t- Freezing :  oooooooooooo (esc)
  fileB\t- Frozen(100%) (esc)

  $ mydd count=200 of=fileA
  200+0 records in
  200+0 records out

  $ touch -d @1469443344 fileA

  $ mydd count=300 of=fileB
  300+0 records in
  300+0 records out

  $ touch -d @0 fileB
  $ lha u archive_file.lzh fileA directoryA fileB directoryB fileC
  
  fileA\t- Freezing :  ............. (esc)
  fileA\t- Freezing :  ooooooooooooo (esc)
  fileA\t- Frozen(100%) (esc)
  
  fileC\t- Freezing :  ................... (esc)
  fileC\t- Freezing :  ooooooooooooooooooo (esc)
  fileC\t- Frozen(100%) (esc)
