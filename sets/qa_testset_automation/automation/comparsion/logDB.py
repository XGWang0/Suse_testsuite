#!/usr/bin/python3

import logging

TableFields = ('release', 'build', 'arch', 'hostname', 'suitename', 'date')

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

class logURLRecord():
    log_class_dict = dict()
    result_class_dict = dict()

    def __init__(self, url):
        self.url = url

import mysql.connector
class logDB():
    @staticmethod
    def _connect(config):
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise LogDBError("%s user name or password is wrong" % config['database'])
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise LogDBError("%s dose NOT exist" % config['database'])
            else:
                raise err
        return cnx
    #TODO cnx.close()

logDB_debug = False

class qaDB(logDB):
    config = {
        'user': 'qadb',
        'password': '',
        'host': '147.2.207.30',
        'database': 'qadb',
        'raise_on_warnings': False,
    }

    def __getattr__(self, name):
        if name == 'cnx':
            self.cnx = self._connect(qaDB.config)
            return self.cnx
        else:
            raise AttributeError(name)

    def get_log_records(self, sql):
        if logDB_debug:
            print("logDB_debug sql is %s" % sql)
        cursor = self.cnx.cursor()
        cursor.execute(sql)
        retl = list()
        for record in cursor:
            if logDB_debug:
                print(record)
            retl.append(record)
        return retl;

#perfDB is not a real DB current.
#it is based on qaDB
# the map between names in perfDB and qaDB
# LogRecord 	tcf_view
#  release   	product
#  build     	release
#  arch      	arch
#  hostname  	host
#  suitename 	testsuite
#  date		test_date

class perfDB():
    def __init__(self):
        self.shadow_db = qaDB()

    def _get_logs(self, release, build, arch, host = None, suite = None, date = None):
        sql = "SELECT `product`,`release`,`arch`,`host`,`testsuite`,`test_date`,`log_url`" \
              " FROM `tcf_view` WHERE `product` = '%s'" \
              " AND `release` = '%s'" \
              " AND `arch` = '%s'" \
              % (release, build, arch)

        if host != None:
            sql += " AND `host` = '%s'" % host
        if suite != None:
            sql += " AND `testsuite` = '%s'" % suite
        if date != None:
            sql += " AND `test_date` = '%s'" % date
        try:
            records = self.shadow_db.get_log_records(sql)
        except Exception as e:
            logging.debug("TODO with the exception")
            logging.error(e)
            raise(e)
        if len(records) == 0:
            logging.warn("got nothing with %s" % sql)
        return records

    def get_log_by_build(self, release, build, arch):
        return self._get_logs(release, build, arch)

    def get_logdir_by_run(self, release, build, arch, host, suite, date = None):
        records = self._get_logs(release, build, arch, host, suite, date)
        rl = list()
        for (release, build, arch, host, suite, date, log_url) in records:
            logging.debug("logdir %s %s" % (suite, log_url))
            
            rl.append(log_url)
        return rl

perfdb_singleton = None
def get_perfdb():
    global perfdb_singleton
    if not perfdb_singleton:
        logging.debug("[logDB] create the perfdb singleton")
        perfdb_singleton = perfDB()
    return perfdb_singleton

# Test Cases
def test_perf_db():
    db = perfDB()
    fields = {}
    fields = db.api_check_get_suite(**fields)
    records = db.get_suite_unchecked(**fields)
    fields = {}
    fields = db.api_check_get_logdir(**fields)
    records = db.get_logdir_unchecked(**fields)

def test_equal():
    a1 = logRecord()
    a2 = logRecord()
    if a1 == a2:
        print('a1 == a2')
    else:
        print('a1 != a2')

if __name__ == '__main__':
    test_equal()
    test_perf_db()
