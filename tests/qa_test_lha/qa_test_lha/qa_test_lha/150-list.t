vim: set sts=2 sw=2 et

list files in  archive
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

  $ mydd count=200 of=directoryB/fileBA
  200+0 records in
  200+0 records out

  $ touch -d @1469513323 archive_file.lzh
 
  $ lha l archive_file.lzh 
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              directoryA/
  -rw-r--r--     0/0       24576 100.0%              directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              directoryB/
  -rw-r--r--     0/0       12288 100.0%              directoryB/fileBA
  -rw-r--r--     0/0       49152 100.0%              fileA
  -rw-r--r--     0/0       98304 100.0%              fileB
  ---------- ----------- ------- ------ ------------ --------------------
   Total         6 files  184320 100.0% Jul 26 06:08

  $ lha -l archive_file.lzh          
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              directoryA/
  -rw-r--r--     0/0       24576 100.0%              directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              directoryB/
  -rw-r--r--     0/0       12288 100.0%              directoryB/fileBA
  -rw-r--r--     0/0       49152 100.0%              fileA
  -rw-r--r--     0/0       98304 100.0%              fileB
  ---------- ----------- ------- ------ ------------ --------------------
   Total         6 files  184320 100.0% Jul 26 06:08

  $ lha archive_file.lzh
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              directoryA/
  -rw-r--r--     0/0       24576 100.0%              directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              directoryB/
  -rw-r--r--     0/0       12288 100.0%              directoryB/fileBA
  -rw-r--r--     0/0       49152 100.0%              fileA
  -rw-r--r--     0/0       98304 100.0%              fileB
  ---------- ----------- ------- ------ ------------ --------------------
   Total         6 files  184320 100.0% Jul 26 06:08
