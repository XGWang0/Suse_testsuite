vim: set sts=2 sw=2 et

create and move files to archive(delete on disk) - validation
------

  $ . $TESTDIR/functions

  $ rm -f archive_file.lzh

  $ cp -r $TESTDIR/static_files $PWD

  $ md5sum ./static_files/fileA ./static_files/directoryA ./static_files/directoryA/fileAA ./static_files/fileB ./static_files/directoryB ./static_files/directoryB/fileBA ./static_files/fileC
  b8aac0b200b52d254c0d6019e94ba62d  ./static_files/fileA
  md5sum: ./static_files/directoryA: Is a directory
  a1f5af19bd7024ef679ab782a3b70867  ./static_files/directoryA/fileAA
  8b12f5d0fe32278685d144c6165e94e8  ./static_files/fileB
  md5sum: ./static_files/directoryB: Is a directory
  f47a4b804edba2e9f006c904600af1f8  ./static_files/directoryB/fileBA
  fc2dd5e63cb3b7ae1dc2fdcfb41f2c01  ./static_files/fileC
  [1]

  $ lha -ad archive_file.lzh ./static_files/fileA ./static_files/directoryA ./static_files/fileB ./static_files/directoryB
  
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
 
  $ lha -x -w=./DIR archive_file.lzh
  
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

  $ lha x -w=./DIR archive_file.lzh
  LHa: Warning: skip to extract ./DIR/static_files/directoryA/fileAA.
  LHa: Warning: skip to extract ./DIR/static_files/directoryB/fileBA.
  LHa: Warning: skip to extract ./DIR/static_files/fileA.
  LHa: Warning: skip to extract ./DIR/static_files/fileB.
  $ md5sum ./DIR/static_files/fileA ./DIR/static_files/directoryA ./DIR/static_files/directoryA/fileAA ./DIR/static_files/fileB ./DIR/static_files/directoryB ./DIR/static_files/directoryB/fileBA ./DIR/static_files/fileC
  b8aac0b200b52d254c0d6019e94ba62d  ./DIR/static_files/fileA
  md5sum: ./DIR/static_files/directoryA: Is a directory
  a1f5af19bd7024ef679ab782a3b70867  ./DIR/static_files/directoryA/fileAA
  8b12f5d0fe32278685d144c6165e94e8  ./DIR/static_files/fileB
  md5sum: ./DIR/static_files/directoryB: Is a directory
  f47a4b804edba2e9f006c904600af1f8  ./DIR/static_files/directoryB/fileBA
  md5sum: ./DIR/static_files/fileC: No such file or directory
  [1]
