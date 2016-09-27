vim: set sts=2 sw=2 et

move files to the archive
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

  $ touch  -d @1469443344 archive_file.lzh

  $ ls -lR
  .:
  total 32
  -rw-r--r-- 1 root root 28363 Jul 25 10:42 archive_file.lzh
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

  $ echo -e "toto je testovaci soubor fileA\n sem patri text\n na nekolika radkach" > ./static_files/fileA

  $ echo -e "toto je testovaci soubor fileB\n sem patri text\n na nekolika radkach" > ./static_files/fileB

  $ touch -d @1469443344 ./static_files/fileA

  $ mydd count=300 of=./static_files/fileB
  300+0 records in
  300+0 records out

  $ touch -d @1 ./static_files/fileB

  $ lha m archive_file.lzh ./static_files/fileA ./static_files/directoryA ./static_files/fileB ./static_files/directoryB ./static_files/fileC
  
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
  static_files/fileA\t- Frozen(88%) (esc)
  
  static_files/fileB\t- Freezing :  ................... (esc)
  static_files/fileB\t- Freezing :  ooooooooooooooooooo (esc)
  static_files/fileB\t- Frozen(100%) (esc)
  
  static_files/fileC\t- Freezing :  . (esc)
  static_files/fileC\t- Freezing :  o (esc)
  static_files/fileC\t- Frozen(100%) (esc)

  $ touch  -d @1469513323 archive_file.lzh

  $ lha l archive_file.lzh
  PERMISSION  UID  GID      SIZE  RATIO     STAMP           NAME
  ---------- ----------- ------- ------ ------------ --------------------
  drwxr-xr-x     0/0           0 ******              static_files/directoryA/
  -rw-r--r--     0/0        7800 100.0%              static_files/directoryA/fileAA
  drwxr-xr-x     0/0           0 ******              static_files/directoryB/
  -rw-r--r--     0/0       11700 100.0%              static_files/directoryB/fileBA
  -rw-r--r--     0/0          68  88.2% Jul 25 10:42 static_files/fileA
  -rw-r--r--     0/0      153600 100.0% Jan  1  1970 static_files/fileB
  -rw-r--r--     0/0        6240 100.0%              static_files/fileC
  ---------- ----------- ------- ------ ------------ --------------------
   Total         7 files  179408 100.0% Jul 26 06:08

  $ ls -lR
  .:
  total 184
  -rw-r--r-- 1 root root 179906 Jul 26 06:08 archive_file.lzh
  drwxr-xr-x 2 root root   4096 * static_files (glob)
  
  ./static_files:
  total 0

