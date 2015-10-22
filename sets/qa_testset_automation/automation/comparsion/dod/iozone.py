#!usr/bin/env python3

import sys
import os
import re

import parserManager

from dod import *
from common import *

import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)
PST_REPORT_S, PST_REPORT_E, PST_RECORD = range(4, 4 + 3)

class DODIOZone(DODLog):
    def __init__(self, stream):
        super(DODIOZone, self).__init__(stream)
        self.ST = PST_NULL
        self.line_num  = 0

    def parse_iopt(self, node):
        reclen = list()
        line = next(self.stream)
        self.line_num += 1
        fields = line.split()
        for f in fields:
            reclen.append(f.strip('"'))
        for line in self.stream:
            self.line_num += 1
            if not re.match('^"\d+"', line):
                break
            try:
                record = line.split()
                fsize = record[0]
                for i in range(2):
                    v = record[i+1]
                    rl = reclen[i]
                    node[fsize][rl] = int(v)
            except IndexError:
                raise LogFormatError("DODIOZone %d" % self.line_num)
            self.ST = PST_RECORD

        if self.ST != PST_RECORD:
            raise LogFormatError("DODIOZone %d" % self.line_num)

    def parse_case(self):
        for line in self.stream:
            self.line_num += 1
            if re.match('^\s*$', line):
                continue
            else:
                self.ST = PST_REPORT_S
                break

        if self.ST != PST_REPORT_S:
            return False

        m = re.match('^"([a-zA-z- ]+) report"$', line)
        if not m: #end of file
            return False
        iopt = m.group(1)
        iopt = iopt.replace(" ","-")
        self.parse_iopt(self._dod[iopt])
        self.ST = PST_REPORT_E
        return True

    def parse(self):
        if self.ST == PST_NULL or self.ST == PST_FAILED:
            for line in self.stream:
                self.line_num += 1
                if re.match('^Excel output is below', line):
                    #logging.debug("DODIOZone parse PST_START")
                    self.ST = PST_START
                    break

        if self.ST == PST_START:
            while self.parse_case():
                pass
            self.ST = PST_DONE
        else:
            self.ST = PST_FAILED
        #TODO check self._dod

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parse()
            return self._dod
        raise AttributeError()

fl = ['qa_iozone_doublemem_ext3','qa_iozone_doublemem_xfs','qa_iozone_doublemem_btrfs','qa_iozone_doublemem_ext4']
tl =['iozone-doublemem-async','iozone-doublemem-fsync']
for i in fl:
    for j in tl:
        parserManager.add_parser("sample",i,j,DODIOZone)

#parserManager.add_parser("sample",
#                         "qa_iozo"ne_doublemem_ext3",
#                         "iozone-"doublemem-async",
#                         DODIOZon"e)
#
#parserManager.add_parser("sample"",
#                         "qa_iozo"ne_doublemem_ext3",
#                         "iozone-"doublemem-fsync",
#                         DODIOZon"e)
