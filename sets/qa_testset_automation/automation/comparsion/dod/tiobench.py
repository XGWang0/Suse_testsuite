#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Sequential Reads', 'Random Reads', 'Sequential Writes', 'Random Writes')
class DODTiobench(DODLog):
    def __init__(self, stream):
        super(DODTiobench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'
        
        for i in IO_PATTERN:
            self._dod[i]=DictOfDict()

    def parse_default(self):
        if self.ST == PST_NULL or self.ST== PST_START:
            for line in self.stream:
                match = re.match(r'^Random Writes\s*|^Sequential Writes\s*|^Random Reads\s*|^Sequential Reads\s*',line)
                record_pt = re.compile(r'^\d\S*\-\w+\s*(\d+\s*\d+\s*\d*)\s*(\d\S*)\s*\d\S*\s*\d\S*\s*(\d\S*)\s*\d\S*\s*\S*')
                if match:
                    read_type = match.group()
                elif record_pt.match(line):
                    self.record(line.strip(),read_type.strip())
                else:
                    self.ST = PST_DONE

    def record(self, line,match):
        results = line.split()
        if match in IO_PATTERN:
            pt_tree=self._dod[match]
            try:
                filesize = results[1]
                if filesize not in pt_tree:
                    pt_tree[filesize]= DictOfDict()
                filesize_tree= pt_tree[filesize]
                block_size =results[2]
                if block_size not in filesize_tree:
                    filesize_tree[block_size]=DictOfDict()
                block_tree= filesize_tree[block_size]

                thread_num =results[3]
                result = results[4]
                if thread_num not in block_tree:
                    block_tree[thread_num]=DictOfDict()
                block_tree[thread_num] = float(result)
            except StopIteration:
                print ('[TiobenchSample] the result has less data than needed')

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parse_default()
                print (self._dod)
            return self._dod
        raise AttributeError()


