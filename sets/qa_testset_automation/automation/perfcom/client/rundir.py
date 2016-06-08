#!/usr/bin/python3

import re
import os
from .error import *
from . import tenv

run_root_dir = "{0}/performance-list".format(os.curdir)

class QASetRunList:
    def __init__(self, stream, tenv_plain):
        self.stream = stream
        self.tenv_plain = tenv_plain
        self.cases = []
        self.parse()

    def parse_array(self):
        for line in self.stream:
            if re.match('^\b*#', line): continue
            if re.match('^$', line): continue
            if re.match('^\b*\)', line):
                self._parse_state = "END"
                return
            self.cases.append(line.strip())

    def parse(self):
        for line in self.stream:
            if re.match('^\b*#', line): continue
            if re.match('^$', line): continue
            if re.match('^\b*SQ_TEST_RUN_LIST=', line):
                self.parse_array()
        if not self._parse_state == "END":
            raise InvalidRunDir("Invalid Run List")

class RunDir:
    def __init__(self, arch, release, build):
        self.run_dir = "{0}/{1}/{2}/{3}".format(run_root_dir, release, arch, build)
        self.arch = arch
        self.release = release
        self.build = build
        self.run_lists = None

    def __iter__(self):
        if not self.run_lists:
            self.scan_dir()
        return iter(self.run_lists)

    def scan_dir(self):
        run_lists = []
        for h in os.listdir(self.run_dir):
            tenv_txt = "{0}/{1}/{2}".format(self.run_dir, h, "tenv.txt")
            if not os.path.isfile(tenv_txt):
                raise InvalidRunDir(tenv_txt)
            perf_list = "{0}/{1}/{2}".format(self.run_dir, h, "performance.list")
            if not os.path.isfile(perf_list):
                raise InvalidRunDir(perf_list)
            stream = open(tenv_txt, "rt")
            tenv_plain = tenv.TenvPlain(stream, tenv_txt, no_category=True)
            stream = open(perf_list, "rt")
            run_lists.append(QASetRunList(stream, tenv_plain))
        self.run_lists = run_lists

