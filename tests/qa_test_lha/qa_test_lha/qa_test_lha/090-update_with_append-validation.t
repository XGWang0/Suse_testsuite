vim: set sts=2 sw=2 et

update archive with append
------

  $ . $TESTDIR/functions

  $ rm -f archive_file.lzh

  $ cp -r $TESTDIR/static_files $PWD

  $ touch -d @0 ./static_files/fileA ./static_files/fileB ./static_files/directoryA ./static_files/directoryA/fileAA ./static_files/directoryB ./static_files/directoryB/fileBA ./static_files/fileC

  $ md5sum ./static_files/fileA ./static_files/directoryA ./static_files/directoryA/fileAA ./static_files/fileB ./static_files/directoryB ./static_files/directoryB/fileBA ./static_files/fileC
  b8aac0b200b52d254c0d6019e94ba62d  ./static_files/fileA
  md5sum: ./static_files/directoryA: Is a directory
  a1f5af19bd7024ef679ab782a3b70867  ./static_files/directoryA/fileAA
  8b12f5d0fe32278685d144c6165e94e8  ./static_files/fileB
  md5sum: ./static_files/directoryB: Is a directory
  f47a4b804edba2e9f006c904600af1f8  ./static_files/directoryB/fileBA
  fc2dd5e63cb3b7ae1dc2fdcfb41f2c01  ./static_files/fileC
  [1]

  $ lha c archive_file.lzh ./static_files/fileA ./static_files/directoryA ./static_files/fileB ./static_files/directoryB
  
  static_files/directoryA/\t- Frozen(0%) (esc)
  
  static_files/directoryA/fileAA\t- Freezing :  . (esc)
  static_files/directoryA/fileAA\t- Freezing :  o (esc)
  static_files/directoryA/fileAA\t- Frozen(100%) (esc)
  
  static_files/directoryB/\t- Frozen(0%) (esc)
  
  static_files/directoryB/fileBA\t- Freezing :  .. (esc)
  static_files/directoryB/fileBA\t- Freezing :  oo (esc)
  static_files/directoryB/fileBA\t- Frozen(100%) (esc)
  
  static_files/fileA\t- Freezing :  . (esc)
  static_files/fileA\t- Freezing :  o (esc)
  static_files/fileA\t- Frozen(100%) (esc)
  
  static_files/fileB\t- Freezing :  . (esc)
  static_files/fileB\t- Freezing :  o (esc)
  static_files/fileB\t- Frozen(100%) (esc)

  $ touch -d @1469443344 archive_file.lzh

  $ mydd count=200 of=fileA
  200+0 records in
  200+0 records out

  $ touch -d @1469443344 fileA

  $ touch -d @0 ./static_files/fileB

  $ lha l archive_file.lzh
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              static_files/directoryA/
  -rw-r--r--     0/0        7800 100.0%              static_files/directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              static_files/directoryB/
  -rw-r--r--     0/0       11700 100.0%              static_files/directoryB/fileBA
  -rw-r--r--     0/0        3744 100.0%              static_files/fileA
  -rw-r--r--     0/0        4680 100.0%              static_files/fileB
  ---------- ----------- ------- ------ ------------ --------------------
   Total         6 files   27924 100.0% Jul 25 10:42
  $ lha a archive_file.lzh fileA ./static_files/directoryA ./static_files/fileB ./static_files/directoryB ./static_files/fileC
  
  static_files/directoryA/\t- Frozen(0%) (esc)
  
  static_files/directoryA/fileAA\t- Freezing :  . (esc)
  static_files/directoryA/fileAA\t- Freezing :  o (esc)
  static_files/directoryA/fileAA\t- Frozen(100%) (esc)
  
  static_files/directoryB/\t- Frozen(0%) (esc)
  
  static_files/directoryB/fileBA\t- Freezing :  .. (esc)
  static_files/directoryB/fileBA\t- Freezing :  oo (esc)
  static_files/directoryB/fileBA\t- Frozen(100%) (esc)
  
  static_files/fileB\t- Freezing :  . (esc)
  static_files/fileB\t- Freezing :  o (esc)
  static_files/fileB\t- Frozen(100%) (esc)
  
  static_files/fileC\t- Freezing :  . (esc)
  static_files/fileC\t- Freezing :  o (esc)
  static_files/fileC\t- Frozen(100%) (esc)
  
  fileA\t- Freezing :  ............. (esc)
  fileA\t- Freezing :  ooooooooooooo (esc)
  fileA\t- Frozen(100%) (esc)

  $ touch -d @1469443344 archive_file.lzh

  $ lha l archive_file.lzh
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              static_files/directoryA/
  -rw-r--r--     0/0        7800 100.0%              static_files/directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              static_files/directoryB/
  -rw-r--r--     0/0       11700 100.0%              static_files/directoryB/fileBA
  -rw-r--r--     0/0        3744 100.0%              static_files/fileA
  -rw-r--r--     0/0        4680 100.0%              static_files/fileB
  -rw-r--r--     0/0        6240 100.0%              static_files/fileC
  -rw-r--r--     0/0      102400 100.0% Jul 25 10:42 fileA
  ---------- ----------- ------- ------ ------------ --------------------
   Total         8 files  136564 100.0% Jul 25 10:42

  $ lha x -w=./DIR archive_file.lzh
  
  ./DIR/static_files/directoryA/fileAA\t- Melting  :  .... (esc)
  ./DIR/static_files/directoryA/fileAA\t- Melting  :  oooo (esc)
  ./DIR/static_files/directoryA/fileAA\t- Melted   (esc)
  
  ./DIR/static_files/directoryB/fileBA\t- Melting  :  ...... (esc)
  ./DIR/static_files/directoryB/fileBA\t- Melting  :  oooooo (esc)
  ./DIR/static_files/directoryB/fileBA\t- Melted   (esc)
  
  ./DIR/static_files/fileA\t- Melting  :  .. (esc)
  ./DIR/static_files/fileA\t- Melting  :  oo (esc)
  ./DIR/static_files/fileA\t- Melted   (esc)
  
  ./DIR/static_files/fileB\t- Melting  :  ... (esc)
  ./DIR/static_files/fileB\t- Melting  :  ooo (esc)
  ./DIR/static_files/fileB\t- Melted   (esc)
  
  ./DIR/static_files/fileC\t- Melting  :  .... (esc)
  ./DIR/static_files/fileC\t- Melting  :  oooo (esc)
  ./DIR/static_files/fileC\t- Melted   (esc)
  
  ./DIR/fileA\t- Melting  :  ......................... (esc)
  ./DIR/fileA\t- Melting  :  ooooooooooooooooooooooooo (esc)
  ./DIR/fileA\t- Melted   (esc)

  $ md5sum ./static_files/fileA ./DIR/static_files/directoryA ./DIR/static_files/directoryA/fileAA ./DIR/static_files/fileB ./DIR/static_files/directoryB ./DIR/static_files/directoryB/fileBA ./DIR/static_files/fileC
  b8aac0b200b52d254c0d6019e94ba62d  ./static_files/fileA
  md5sum: ./DIR/static_files/directoryA: Is a directory
  a1f5af19bd7024ef679ab782a3b70867  ./DIR/static_files/directoryA/fileAA
  8b12f5d0fe32278685d144c6165e94e8  ./DIR/static_files/fileB
  md5sum: ./DIR/static_files/directoryB: Is a directory
  f47a4b804edba2e9f006c904600af1f8  ./DIR/static_files/directoryB/fileBA
  fc2dd5e63cb3b7ae1dc2fdcfb41f2c01  ./DIR/static_files/fileC
  [1]
