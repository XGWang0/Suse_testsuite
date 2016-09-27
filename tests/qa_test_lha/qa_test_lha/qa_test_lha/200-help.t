vim: set sts=2 sw=2 et

help
------

  $ lha --help
  LHarc    for UNIX  V 1.02  Copyright(C) 1989  Y.Tagawa
  LHx      for MSDOS V C2.01 Copyright(C) 1990  H.Yoshizaki
  LHx(arc) for OSK   V 2.01  Modified     1990  Momozou
  LHa      for UNIX  V 1.00  Copyright(C) 1992  Masaru Oki
  LHa      for UNIX  V 1.14  Modified     1995  Nobutaka Watazaki
  LHa      for UNIX  V 1.14i Modified     2000  Tsugio Okamoto
                     Autoconfiscated 2001-2008  Koji Arai
  usage: lha [-]<commands>[<options>] [-<options> ...] archive_file [file...]
    commands:  [axelvudmcpt]
    options:   [q[012]vnfto[567]dizg012e[w=<dir>|x=<pattern>]]
    long options: --system-kanji-code={euc,sjis,utf8,cap}
                  --archive-kanji-code={euc,sjis,utf8,cap}
                  --extract-broken-archive
                  --convert-filename-case
  \t\t--ignore-mac-files (esc)
                  --traditional
                  --help
                  --version
  commands:                           options:
   a   Add(or replace) to archive      q{num} quiet (num:quiet mode)
   x,e EXtract from archive            v  verbose
   l,v List / Verbose List             n  not execute
   u   Update newer files to archive   f  force (over write at extract)
   d   Delete from archive             t  FILES are TEXT file
   m   Move to archive (means 'ad')    o[567] compression method (a/u/c)
   c   re-Construct new archive        d  delete FILES after (a/u/c)
   p   Print to STDOUT from archive    i  ignore directory path (x/e)
   t   Test file CRC in archive        z  files not compress (a/u/c)
                                       g  Generic format (for compatibility)
                                       0/1/2 header level (a/u/c)
                                       e  TEXT code convert from/to EUC
                                       w=<dir> specify extract directory (x/e)
                                       x=<pattern>  eXclude files (a/u/c)

