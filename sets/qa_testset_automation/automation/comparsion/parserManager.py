import logging
import dod
import urllib
import urllib.request
import io

__all__ = []

class Error(Exception):
    pass

class Manager:
    def __init__(self, name, parser_cls):
        self.name = name
        self.parser = dict()
        self.parser_cls = parser_cls

    def contains(self, suite, case):
        if not suite in self.parser:
            return False
        else:
            parser = self.parser[suite]
        if not case in parser:
            return False
        else:
            return True

    def add_parser(self, suite, case, cls):
        ''' Add a parser to the manager '''
        if not issubclass(cls, self.parser_cls):
            raise Error("%s is not a %s" % type(cls), type(self.parser_cls))
        if not suite in self.parser:
            self.parser[suite] = dict()
        parser = self.parser[suite]
        parser[case] = cls
        logging.debug("[ParserManager] %s adds %s %s" % (self.name, suite, case))

    def get_parser(self, suite, case = None):
        ''' Return a parser '''
        if not suite in self.parser:
            logging.warning("manager %s dose NOT have parser for %s" % suite)
            return None
        parser = self.parser[suite]
        if not case:
            return parser
        elif case in parser:
            return parser[case]
        else:
            logging.warning("suite %s dose NOT have %s" % (suite, case))
            return None

def save_tmp(response):
    print("type of response %s" % type(response))
    #allstr = response.read().decode('utf-8')
    for line in t:
        print(line)

def _download_url(url):
    response = urllib.request.urlopen(url)
    g = io.BufferedReader(response)
    t = io.TextIOWrapper(g, "utf-8")
    return t

class ManagerSample(Manager):
    def get_statistic_from_urls(self, suite, case, urls):
        parserClass = self.get_parser(suite, case)
        if not parserClass:
            raise Error("no sample parser for %s %s" % (suite, case))
        loglist = dod.DODLogList(None)
        for url in urls:
            try:
                stream = _download_url(url)
                log = parserClass(stream)
                loglist.append(log.dod)
            except Exception as e:
                logging.error(e)
                raise(e)
        return loglist.statistic()

class ManagerList(Manager):
    def get_statistic_from_urls(self, suite, case, urls):
        parserClass = self.get_parser(suite, case)
        if not parserClass:
            raise Error("no list parser for %s %s" % (suite, case))
        if len(urls) > 1:
            logging.warning("list parser more than one log")
        try:
            stream = _download_url(urls[0])
            loglist = parserClass(stream)
        except Exception as e:
            logging.error(e)
            raise(e)
        return loglist.statistic()

class ManagerStatistic(Manager):
    def get_statistic_from_urls(self, suite, case, urls):
        parserClass = self.get_parser(suite, case)
        if not parserClass:
            raise Error("no statistic parser for %s %s" % (suite, case))
        try:
            stream = _download_url(urls[0])
            log = parserClass(stream)
        except Exception as e:
            logging.error(e)
            raise(e)
        return log()

Sample = ManagerSample("sample", dod.DODLog)
List = ManagerList("list", dod.DODLogList)
Statistic = ManagerStatistic("stat", dod.DODLogStatistic)

all_managers = set((Sample, List, Statistic))

def add_parser(manager_name, suite, case, cls):
    err_msg = "Conflict: parser for suite and case in %s"
    manager = None
    if manager_name == "sam" or \
       manager_name == "sample":
        manager = Sample
    elif Sample.contains(suite, case):
        raise(Error(err_msg % Sample.name))

    if manager_name == "list":
        manager = List
    elif List.contains(suite, case):
        raise(Error(err_msg % Sample.name))

    if manager_name == "stat" or \
       manager_name == "statistic":
        manager = Statistic
    elif Statistic.contains(suite, case):
        raise(Error(err_msg % Sample.name))

    if not manager:
        raise(Error("no parser named %s" % manager_name))

    manager.add_parser(suite, case, cls)

def get_statistic_from_urls(suite, case, urls):
    for manager in all_managers:
        if manager.contains(suite, case):
            return manager.get_statistic_from_urls(suite, case, urls)
    raise(Error("no parser for %s %s" % (suite, case)))

