vim: set sts=2 sw=2 et

move files to the archive
------

  $ . $TESTDIR/functions

  $ rm -f archive_file.lzh

  $ cp -r $TESTDIR/static_files $PWD

  $ touch -d @0 ./static_files/fileA ./static_files/fileB ./static_files/directoryA ./static_files/directoryA/fileAA ./static_files/directoryB ./static_files/directoryB/fileBA ./static_files/fileC

  $ lha c archive_file.lzh ./static_files/fileA ./static_files/directoryA ./static_files/fileB ./static_files/directoryB ./static_files/fileC
  
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
  
  static_files/fileC\t- Freezing :  . (esc)
  static_files/fileC\t- Freezing :  o (esc)
  static_files/fileC\t- Frozen(100%) (esc)

  $ touch  -d @1469443344 archive_file.lzh

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
  ---------- ----------- ------- ------ ------------ --------------------
   Total         7 files   34164 100.0% Jul 25 10:42

deletes only files not dirs
  $ lha d archive_file.lzh ./static_files/directoryB static_files/fileC
  LHa: delete static_files/fileC

  $ touch  -d @1469513323 archive_file.lzh

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
   Total         6 files   27924 100.0% Jul 26 06:08

  $ ls -lR
  .:
  total 32
  -rw-r--r-- 1 root root 28363 Jul 26 06:08 archive_file.lzh
  drwxr-xr-x 4 root root  4096 * static_files (glob)
  
  ./static_files:
  total 28
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root 3744 Jan  1  1970 fileA
  -rw-r--r-- 1 root root 4680 Jan  1  1970 fileB
  -rw-r--r-- 1 root root 6240 Jan  1  1970 fileC
  
  ./static_files/directoryA:
  total 8
  -rw-r--r-- 1 root root 7800 Jan  1  1970 fileAA
  
  ./static_files/directoryB:
  total 12
  -rw-r--r-- 1 root root 11700 Jan  1  1970 fileBA

