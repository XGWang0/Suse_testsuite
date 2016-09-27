vim: set sts=2 sw=2 et

print content of files in archive
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

  $ lha p archive_file.lzh
  ::::::::
  directoryA/fileAA
  ::::::::
  toto je testovaci soubor directoryA fileAA 
   sem patri text
   na nekolika radkach
  ::::::::
  directoryB/fileBA
  ::::::::
  toto je testovaci soubor directoryB fileBA 
   sem patri text se symboly
   +i<>*\xc4\x90[] `{}<>*$\xc5\x82'']\xe2\x86\x90\xc5\x81%^&{{}@!%! (esc)
  ::::::::
  fileA
  ::::::::
  toto je testovaci soubor fileA
   sem patri text
   na nekolika radkach
  ::::::::
  fileB
  ::::::::
  toto je testovaci soubor fileB
   sem patri text
   na nekolika radkach
