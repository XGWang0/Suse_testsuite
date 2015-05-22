import urllib.request
from urllib.parse import urlparse
from html.parser import HTMLParser
import re
import os

import urllib.request

import common
from logDB import *

import logging

__all__ = ['QADBRecord', 'QADBGroup']

class QADBError(common.Error):
    def __init__(self, msg):
        self.msg = msg

class HiHTMLParser(HTMLParser):
    def hi_reset(self):
        self.ipt = re.compile(r'\?C=.;O=.')
        self.dpt = re.compile(r'/')
        self.file_list = list()
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for a in attrs:
                if a[0] == 'href':
                    if self.dpt.match(a[1]) or self.ipt.match(a[1]):
                        return
                    else:
                        self.file_list.append(a[1])
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

def _parse_the_html(stream):
        parse = HiHTMLParser()
        parse.hi_reset()
        parse.feed(stream)
        return parse.file_list

class QADBRecord(logRecord):
    def __init__(self, url):
        self.url = url
        self._fields()

    def _fields(self):
        ucom = urlparse(self.url)
        upath_list = ucom.path.split('/')
        i = -1
        try:
            basename = upath_list[i]
            i -= 1
            if len(basename) == 0:
                basename = upath_list[i]
                i -= 1
                hostname = upath_list[i]; i -= 1
                arch = upath_list[i]; i -= 1
                build = upath_list[i]; i -= 1
                release  = upath_list[i]; i -= 1
        except IndexError:
            raise QADBError('bad URL format')

        m = re.match('^(.*)-(20\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})$', basename)
        if not m:
            raise QADBError('bad URL format')
        suitename = m.group(1)
        date = m.group(2)
        self.init_fields({'release': release, 'build': build,
                          'arch': arch, 'hostname' : hostname,
                          'suitename': suitename, 'date':date})

    def download(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            response = urllib.request.urlopen(self.url)
            file_list = _parse_the_html(response.read().decode('utf-8'))
            for f in file_list:
                furl = "%s/%s" % (self.url, f)
                fpath = "%s/%s" % (path, f)
                fd = open(fpath, "wb")
                fd.write(urllib.request.urlopen(furl).read())
                fd.close()
        except URLError as E:
            logger.error(E)
            return False
        except Exception as E:
            raise E
        logging.debug("Download Done %s" % self.url)

class QADBGroup(logGroup):
    def __init__(self, url_list):
        self.records = list()
        self.transaction('append')
        for url in url_list:
            self._append(url)
        self.commit()

    def transaction(self, action):
        self.action = action
        if action == 'append':
            pass

    def commit(self):
        if self.action == 'append':
            if len(self.records) == 0: return None
            first = self.records[0]
            for r in self.records[1:]:
                if first != r:
                    s1 = str(first)
                    s2 = str(r)
                    raise QADBError("the QADB group is not consistant\n%s\n%s" % (s1, s2))
            self.clear()
            self.init_fields(first)
        self.action = None

    def _append(self, url):
        self.records.append(QADBRecord(url))

    def append(self, url):
        self.transaction('append')
        self._append(url)
        self.commit()

    def download(self, path):
        for r in self.records:
            p  = path + '/' + r['date']
            r.download(path + '/' + r['date'])
