#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import parserManager
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Thread', 'Throughput')
class DODDbench(DODLog):
    def __init__(self, stream):
        super(DODDbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 'b'        
        #for i in IO_PATTERN:
        self._dod=DictOfDict()

    def parser(self):
        thread = []
        value = [] 
        if self.ST == PST_NULL or self.ST== PST_START:
            for line in self.stream:
                tmatch = re.match(r'^dbench\s*(\-[a-z,A-Z]*\s)*\d*\s*\-[A-Z]\s*\/[a-z]*\s*(\d*)',line)
                vmatch = re.match(r'^Throughput\s*(\d*\.?\d*)',line)
                if tmatch:
                    thread.append(tmatch.group(2))
                    continue
                elif vmatch:
                    value.append(vmatch.group(1))
                else:
                    pass
        if len(thread) ==len(value):
            for i in range(len(thread)):
                if not value[i]:
                    self._dod[thread[i]]= 0
                else:
                    self._dod[thread[i]]=float(value[i])

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

parserManager.add_parser("sample",
                         "dbench4_async_btrfs",
                         "dbench4-async",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_async_ext3",
                         "dbench4-async",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_async_ext4",
                         "dbench4-async",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_async_xfs",
                         "dbench4-async",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_fsync_btrfs",
                         "dbench4-fsync",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_fsync_ext3",
                         "dbench4-fsync",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_fsync_xfs",
                         "dbench4-fsync",
                         DODDbench)

parserManager.add_parser("sample",
                         "dbench4_fsync_ext4",
                         "dbench4-fsync",
                         DODDbench)

