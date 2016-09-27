vim: set sts=2 sw=2 et

extract files from archive to directory
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

  $ touch -d @1469513323 fileA directoryB/fileBA

  $ ls -lR
  .:
  total 552
  -rw-r--r-- 1 root root 184675 * archive_file.lzh (glob)
  drwxr-xr-x 2 root root   4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root   4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root 102400 Jul 26 06:08 fileA
  -rw-r--r-- 1 root root  98304 Jan  1  1970 fileB
  -rw-r--r-- 1 root root 148480 Jan  1  1970 fileC
  
  ./directoryA:
  total 24
  -rw-r--r-- 1 root root 24576 Jan  1  1970 fileAA
  
  ./directoryB:
  total 104
  -rw-r--r-- 1 root root 102400 Jul 26 06:08 fileBA

  $ lha -x -w=./DIR archive_file.lzh 
  
  ./DIR/directoryA/fileAA\t- Melting  :  ............ (esc)
  ./DIR/directoryA/fileAA\t- Melting  :  oooooooooooo (esc)
  ./DIR/directoryA/fileAA\t- Melted   (esc)
  
  ./DIR/directoryB/fileBA\t- Melting  :  ...... (esc)
  ./DIR/directoryB/fileBA\t- Melting  :  oooooo (esc)
  ./DIR/directoryB/fileBA\t- Melted   (esc)
  
  ./DIR/fileA\t- Melting  :  ........................ (esc)
  ./DIR/fileA\t- Melting  :  oooooooooooooooooooooooo (esc)
  ./DIR/fileA\t- Melted   (esc)
  
  ./DIR/fileB\t- Melting  :  ........................ (esc)
  ./DIR/fileB\t- Melting  :  oooooooooooooooooooooooo (esc)
  ./DIR/fileB\t- Melted   (esc)

  $ touch -d @1469513323 ./DIR archive_file.lzh

  $ ls -lR
  .:
  total 556
  drwxr-xr-x 4 root root   4096 Jul 26 06:08 DIR
  -rw-r--r-- 1 root root 184675 Jul 26 06:08 archive_file.lzh
  drwxr-xr-x 2 root root   4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root   4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root 102400 Jul 26 06:08 fileA
  -rw-r--r-- 1 root root  98304 Jan  1  1970 fileB
  -rw-r--r-- 1 root root 148480 Jan  1  1970 fileC
  
  ./DIR:
  total 156
  drwxr-xr-x 2 root root  4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root  4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root 49152 Jan  1  1970 fileA
  -rw-r--r-- 1 root root 98304 Jan  1  1970 fileB
  
  ./DIR/directoryA:
  total 24
  -rw-r--r-- 1 root root 24576 Jan  1  1970 fileAA
  
  ./DIR/directoryB:
  total 12
  -rw-r--r-- 1 root root 12288 Jan  1  1970 fileBA
  
  ./directoryA:
  total 24
  -rw-r--r-- 1 root root 24576 Jan  1  1970 fileAA
  
  ./directoryB:
  total 104
  -rw-r--r-- 1 root root 102400 Jul 26 06:08 fileBA
