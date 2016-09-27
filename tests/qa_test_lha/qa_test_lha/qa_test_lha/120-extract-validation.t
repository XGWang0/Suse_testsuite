vim: set sts=2 sw=2 et

extract files from archive 
------

  $ . $TESTDIR/functions

  $ rm -f archive_file.lzh

  $ echo -e "toto je testovaci soubor fileA\n sem patri text\n na nekolika radkach" > fileA

  $ echo -e "toto je testovaci soubor fileB\n sem patri text\n na nekolika radkach" > fileB

  $ echo -e "toto je testovaci soubor fileC\n sem patri text\n na nekolika radkach" > fileC

  $ mkdir directoryA directoryB

  $ echo -e "toto je testovaci soubor directoryA fileAA \n sem patri text\n na nekolika radkach" > directoryA/fileAA

  $ echo -e "toto je testovaci soubor directoryB fileBA \n sem patri text se symboly\n +i<>*Đ[] \`{}<>*$ł'']←Ł%^&{{}@!%!" > directoryB/fileBA

  $ touch -d @0 fileA fileB directoryA directoryA/fileAA directoryB directoryB/fileBA fileC

  $ lha c archive_file.lzh fileA directoryA fileB directoryB
  
  directoryA/\t- Frozen(0%) (esc)
  
  directoryA/fileAA\t- Freezing :  . (esc)
  directoryA/fileAA\t- Freezing :  o (esc)
  directoryA/fileAA\t- Frozen(82%) (esc)
  
  directoryB/\t- Frozen(0%) (esc)
  
  directoryB/fileBA\t- Freezing :  . (esc)
  directoryB/fileBA\t- Freezing :  o (esc)
  directoryB/fileBA\t- Frozen(100%) (esc)
  
  fileA\t- Freezing :  . (esc)
  fileA\t- Freezing :  o (esc)
  fileA\t- Frozen(88%) (esc)
  
  fileB\t- Freezing :  . (esc)
  fileB\t- Freezing :  o (esc)
  fileB\t- Frozen(88%) (esc)

  $ touch -d @1469443344 archive_file.lzh

  $ md5sum fileA directoryA directoryA/fileAA fileB directoryB directoryB/fileBA fileC
  cd6b6b48c18aba14ff604849eb71e2a8  fileA
  md5sum: directoryA: Is a directory
  78018da6e1e7ece2b598c42043bc0d6e  directoryA/fileAA
  65e6545c72bf2764fec28a5249205e44  fileB
  md5sum: directoryB: Is a directory
  75cc022b0d0f4b6c8c8b4a54d5000e4a  directoryB/fileBA
  70d07ef1c47d9b7c5027d735d90cc89f  fileC
  [1]

  $ ls -lR
  .:
  total 24
  -rw-r--r-- 1 root root  652 Jul 25 10:42 archive_file.lzh
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileA
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileB
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileC
  
  ./directoryA:
  total 4
  -rw-r--r-- 1 root root 81 Jan  1  1970 fileAA
  
  ./directoryB:
  total 4
  -rw-r--r-- 1 root root 110 Jan  1  1970 fileBA

  $ lha x -w=./DIR archive_file.lzh
  
  ./DIR/directoryA/fileAA\t- Melting  :  . (esc)
  ./DIR/directoryA/fileAA\t- Melting  :  o (esc)
  ./DIR/directoryA/fileAA\t- Melted   (esc)
  
  ./DIR/directoryB/fileBA\t- Melting  :  . (esc)
  ./DIR/directoryB/fileBA\t- Melting  :  o (esc)
  ./DIR/directoryB/fileBA\t- Melted   (esc)
  
  ./DIR/fileA\t- Melting  :  . (esc)
  ./DIR/fileA\t- Melting  :  o (esc)
  ./DIR/fileA\t- Melted   (esc)
  
  ./DIR/fileB\t- Melting  :  . (esc)
  ./DIR/fileB\t- Melting  :  o (esc)
  ./DIR/fileB\t- Melted   (esc)

  $ ls -lR
  .:
  total 28
  drwxr-xr-x 4 root root 4096 * DIR (glob)
  -rw-r--r-- 1 root root  652 Jul 25 10:42 archive_file.lzh
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileA
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileB
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileC
  
  ./DIR:
  total 16
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryA
  drwxr-xr-x 2 root root 4096 Jan  1  1970 directoryB
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileA
  -rw-r--r-- 1 root root   68 Jan  1  1970 fileB
  
  ./DIR/directoryA:
  total 4
  -rw-r--r-- 1 root root 81 Jan  1  1970 fileAA
  
  ./DIR/directoryB:
  total 4
  -rw-r--r-- 1 root root 110 Jan  1  1970 fileBA
  
  ./directoryA:
  total 4
  -rw-r--r-- 1 root root 81 Jan  1  1970 fileAA
  
  ./directoryB:
  total 4
  -rw-r--r-- 1 root root 110 Jan  1  1970 fileBA

  $ md5sum ./DIR/fileA ./DIR/directoryA ./DIR/directoryA/fileAA ./DIR/fileB ./DIR/directoryB ./DIR/directoryB/fileBA ./DIR/fileC
  cd6b6b48c18aba14ff604849eb71e2a8  ./DIR/fileA
  md5sum: ./DIR/directoryA: Is a directory
  78018da6e1e7ece2b598c42043bc0d6e  ./DIR/directoryA/fileAA
  65e6545c72bf2764fec28a5249205e44  ./DIR/fileB
  md5sum: ./DIR/directoryB: Is a directory
  75cc022b0d0f4b6c8c8b4a54d5000e4a  ./DIR/directoryB/fileBA
  md5sum: ./DIR/fileC: No such file or directory
  [1]
