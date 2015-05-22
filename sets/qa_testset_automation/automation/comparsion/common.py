import logging
logging.basicConfig(level=logging.DEBUG, datefmt='%H:%M:%S')

class dictOfList(dict):
    def __missing__(self, key):
        self[key] = list()
        return self[key]

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg

class LogFormatError(Error):
    pass


