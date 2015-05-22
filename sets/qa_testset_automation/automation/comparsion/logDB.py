#!/usr/bin/python3

TableFields = ('release', 'build', 'arch', 'hostname', 'suitename', 'date')

import logging

class logRecord(dict):
    @classmethod
    def is_valid_key(cls, k):
        return k in TableFields

    def init_fields(self, fields):
        for k in fields:
            if self.is_valid_key(k):
                self[k] = fields[k]

    def __eq__(self, other):
        for k in self:
            if k == 'date': continue
            if k == 'build':
                if self[k] == other[k]: continue
                gmstr = ('GM', 'GMC')
                if self[k] in gmstr and other[k] in gmstr:
                    continue
            if self[k] != other[k]:
                logging.debug('logRecord key %s is not equal' % k)
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def is_comparable(self, other):
        for k in self:
            if k in ('date', 'build'): continue
            if k == 'release' and self[k] == other[k]:
                return False
            if self[k] != other[k]:
                return False
        return True

class logGroup(dict):
    @classmethod
    def is_valid_key(cls, k):
        if k == 'date': return False
        return k in TableFields

    def init_fields(self, fields):
        for k in fields:
            if self.is_valid_key(k):
                self[k] = fields[k]

    def is_comparable(self, other):
        for k in self:
            if k in ('date', 'build'): continue
            if k == 'release' and self[k] == other[k]:
                return False
            if self[k] != other[k]:
                return False
            return True

if __name__ == '__main__':
    a1 = logRecord()
    a2 = logRecord()
    if a1 == a2:
        print('a1 == a2')
    else:
        print('a1 != a2')
