# LogDir TEST_TARGET/REALEASE/BUILD/ARCH/HOSTNAME/TEST_PROFILE/
#        ext3       /SLE12SP1/Beta3/x86_64/apacII-ph026/iozone-default-20150504-020304/
# system call       /SLE12SP1/Beta3/x86_64/apacII-ph026/iozone-default-20150504-060708/

import os
from dod import dictOfList
from common import *
from logDB import *
import re

class LogDir():
    def __init__(self, root):
        self.root = root

    def __getattr__(self, name):
        if name == 'path':
            self._path()
            return self.path
        raise AttributeError("object has no attribute %s" % name)

    def _path(self):
        self.path =  self.root

class LogDirComponent():
    def __init__(self, logdir, name):
        self.logdir = logdir
        self.name = name

    def __getattr__(self, name):
        if name == 'path':
            self._path()
            return self.path
        raise AttributeError("object has no attribute %s" % name)

    def _path(self):
        self.path = "%s/%s" % (self.logdir.path, self.name)

class logDirRecord(logRecord):
    def __init__(self, log_dir_component, fields):
        self.compoment = log_dir_component
        self.init_fields(fields)

    def __getattr__(self, name):
        if name == 'path':
            self._path()
            return self.path
        raise AttributeError("object has no attribute %s" % name)

    def _path(self):
        path = "%s/%s/%s/%s/%s/%s/%s" % (
            self.compoment.path,
            self['release'],
            self['build'],
            self['arch'],
            self['hostname'],
            self['suitename'],
            self['date']
        )
        self.path = path

    def _logs(self):
        '''
        {file1: dodClass, file2: dodClass}
        '''
        raise NotImplemented()
    

class logDirRecordGroup(logGroup):
    def __init__(self, log_dir_component, fields, recordClass):
        self.compoment = log_dir_component
        self.init_fields(fields)
        self.records = list()
        self.recordClass = recordClass
        self.dod_class_dict = recordClass.dod_class_dict

    def __getattr__(self, name):
        if name == 'path':
            self._path()
            return self.path
        if name == 'logs':
            self._logs()
            return self.logs
        raise AttributeError("object has no attribute %s" % name)

    def _path(self):
        path = "%s/%s/%s/%s/%s/%s" % (
            self.compoment.path,
            self['release'],
            self['build'],
            self['arch'],
            self['hostname'],
            self['suitename']
        )
        self.path = path

    def scan_records(self):
        for f in os.listdir(self.path):
            if not re.match('^20\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$', f):
                continue
            if not os.path.isdir(self.path + '/' + f):
                continue
            r = self.recordClass(self.compoment, self)
            r['date'] = f
            self.records.append(r)

    def _logs(self):
        logs = dictOfList()
        self.scan_records()
        for r in self.records:
            for l in r.logs:
                logs[l].append(r.logs[l])
        self.logs = logs

