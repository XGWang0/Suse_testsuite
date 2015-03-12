#!/usr/bin/env python3

import sys
import os
import re
import math
import logging
import argparse
from namedtree import NamedTree, NamedTreeGroup, OP_KIND_LEAF, OP_KIND_DIR
import ctcs2

log = logging.getLogger()

IO_PATTERN = ('write', 'rewrite', 'read', 'reread', 'random read', 'random write',
              'bkwd read', 'record rewirte', 'stride read', 'fwrite', 'frewrite',
              'fread', 'freread')

PST_NULL, PST_ERROR, PST_START, PST_RECORD, PST_END = range(5)
class IOzoneSample(NamedTree):

    def __init__(self, filename, name = None):
        self.filename = filename
        if not name:
            super().__init__(filename)
        else:
            super().__init__(name)

        tree = {}
        self.tree = tree

        self.fd = None
        self.parse_ST = PST_NULL

    def record(self, line):
        results = line.split()
        results_iter = iter(results)
        KB = int(next(results_iter))     #0
        reclen = int(next(results_iter)) #1

        for pt in IO_PATTERN:
            pt_tree = self.tree[pt]
            try:
                result = next(results_iter)
                if KB not in pt_tree:
                    pt_tree[KB] = dict()
                KB_tree = pt_tree[KB]
                if reclen not in KB_tree:
                    KB_tree[reclen] = int(result) #except?
                else:
                    log.waring('[IOzoneSample] duplicate result %s %s %s %s' % (pt, KB, reclen, result))
            except StopIteration:
                log.warning('[IOzoneSample] the result has less data than needed')
                break

    def parse_default(self):
        if self.parse_ST == PST_NULL:
            self.fd = open(self.filename)
            for pt in IO_PATTERN:
                self.tree[pt] = dict()
            self.parse_ST = PST_START

        if self.parse_ST == PST_START:
            for line in self.fd:
                if re.match('^\s*KB\s+reclen', line):
                    log.debug('[IOzoneSample] [parse_default] find KB reclen line')
                    self.parse_ST = PST_RECORD
                    break

        if self.parse_ST == PST_RECORD:
            record_pt = re.compile('^\s*\d+\s+\d+(\s+\d+)+')
            for line in self.fd:
                if record_pt.match(line):
                    log.debug('[IOzoneSample] [parse_default] find a record %s' % line)
                    self.record(line)
                else:
                    self.parse_ST = PST_END


def main():
    cmdlineparser = argparse.ArgumentParser(description = 'Sample Parser', prog = 'Sample')
    cmdlineparser.add_argument('db', nargs='+')

    #TODO a universal command line

    ns = cmdlineparser.parse_args(sys.argv[1:])
    if len(ns.db) < 0:
        print('Usages')
        exit()

    average_list = []

    for db in ns.db:
        DB = ctcs2.LogDB(db)
        db = DB.samples('qa_iozone_4-32G', 'qa_iozone_4-32G', IOzoneSample)
        if len(db) == 0:
            log.warning('[IOzone] There is no log files from %s' % db)
            continue
        for t in db:
            t.parse_default()
        group = NamedTreeGroup(*db)
        average = group.average()
        average.name = DB.name
        average_list.append(average)

    def note_over_10_percent (v_list):
        if v_list[0] < -0.1:
            return '***'
        else:
            return '   '

    a_iter = iter(average_list)
    r_base = next(a_iter)
    r_list = list()
    r_list.append(r_base)
    spec_end = {r_base.name:'.0f'}
    field_suffix = {}
    while True:
        try:
            r_this = next(a_iter)
        except StopIteration:
            break
        else:
            r_diff_ratio = NamedTree.Operator.diff_ratio(r_base, r_this)
            r_diff_ratio_percent = NamedTree.Operator.scale_multiply(r_diff_ratio, scale = 100)
            r_diff_ratio_percent.name = 'Fluctuation'
            r_diff_ratio_note = NamedTree.Operator.user_defined(r_diff_ratio, cb_func = note_over_10_percent)
            r_diff_ratio_note.name = 'ratio_note'
            
            spec_end[r_this.name] = '.0f'
            spec_end[r_diff_ratio_percent.name] = '.2f'
            spec_end[r_diff_ratio_note.name] = 's'
            field_suffix[r_diff_ratio_percent.name] = " %"
            r_list.append(r_this)
            r_list.append(r_diff_ratio_percent)
            r_list.append(r_diff_ratio_note)

    ngroup = NamedTreeGroup(*r_list)
    ngroup.leaf_render.set_field_format_spec_end(**spec_end)
    ngroup.leaf_render.set_field_suffix(**field_suffix)
    ngroup.leaf_print()

if __name__ == '__main__':
    main()
