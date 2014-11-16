#!/usr/bin/env python3

import sys
import os
import re
import math
import logging
import argparse
import pprint
from namedtree import NamedTree, NamedTreeGroup, OP_KIND_LEAF, OP_KIND_DIR
import ctcs2

log = logging.getLogger()

IO_PATTERN = ('Sequential Reads', 'Random Reads', 'Sequential Writes', 'Random Writes')

PST_NULL, PST_ERROR, PST_START, PST_RECORD, PST_END = range(5)

class TiobenchSample(NamedTree):
    def __init__(self, filename, name = None):
        self.filename = filename
        self.fd = None
        if not name:
            super().__init__(filename)
        else:
            super().__init__(name)
        tree={}
        for i in IO_PATTERN:
           tree[i]={}
        
        self.tree=tree
        
        self.fd = None
        self.parse_ST = PST_NULL

    def parse_default(self):
        if self.parse_ST == PST_NULL:
            self.fd = open(self.filename)
            lines=[]
            lines=[line.strip() for line in self.fd.readlines()]
            self.fd.close()
            #for pt in IO_PATTERN:
                #self.tree[pt] = dict()
            self.parse_ST = PST_START


        if self.parse_ST == PST_START:
            result_tree={}
            for line in lines:
                match = re.match(r'^Random Writes\s*|^Sequential Writes\s*|^Random Reads\s*|^Sequential Reads\s*',line)
                record_pt = re.compile(r'^\d\S*\-\w+\s*(\d+\s*\d+\s*\d*)\s*(\d\S*)\s*\d\S*\s*\d\S*\s*(\d\S*)\s*\d\S*\s*\S*')
                if match:
                    read_type = match.group()
                    #result_tree[match] ={}
                    log.debug('[TiobenchSample] [parse_default] find data line')
                    self.parse_ST = PST_RECORD
                          
                #record_pt = re.compile(r'^\d\S*\-\w+\s*(\d+\s*\d+\s*\d*)\s*(\d\S*)\s*\d\S*\s*\d\S*\s*(\d\S*)\s*\d\S*\s*\S*')
                   
                elif record_pt.match(line):
                    log.debug('[TiobenchSample] [parse_default] find a record %s' % line)
                    self.record(line,read_type)
                else:
                    self.parse_ST = PST_END
             

        #if self.parse_ST == PST_RECORD:
            #record_pt = re.compile(r'^\d\S*\-\w+\s*(\d+\s*\d+\s*\d*)\s*(\d\S*)\s*\d\S*\s*\d\S*\s*(\d\S*)\s*\d\S*\s*\S*')
            #for line in lines:
                #if record_pt.match(line):
                    #log.debug('[TiobenchSample] [parse_default] find a record %s' % line)
                    #self.record(line,read_type)
                #else:
                    #self.parse_ST = PST_END

    def record(self, line,match):
        results = line.split()
        if match in IO_PATTERN:
            pt_tree=dict()
            pt_tree=self.tree[match]
            print(pt_tree)
            try:
                filesize = results[1]
                if filesize not in pt_tree:
                    pt_tree[filesize]= dict()
                filesize_tree= pt_tree[filesize]
                #print (filesize_tree)
                block_size =results[2]
                if block_size not in filesize_tree:
                    filesize_tree[block_size]=dict()
                block_tree= filesize_tree[block_size]
                
                thread_num =results[3]
                result = results[4]
                if thread_num not in block_tree:
                    block_tree[thread_num]={}
                block_tree[thread_num] = float(result)
                # else:
                #    log.waring('[TiobenchSample] duplicate result %s %s %s %s %s' % (pt,filesize, blocksize,thread_number,result))
            except StopIteration:
                log.warning('[TiobenchSample] the result has less data than needed')
               # break


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
        db = DB.samples('tiobench-bench', 'tiobench', TiobenchSample)
        if len(db) == 0:
            log.warning('[tiobench] There is no log files from %s' % DB.name)
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
    spec_end = {r_base.name:'.2f'}
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

            spec_end[r_this.name] = '.2f'
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
            
