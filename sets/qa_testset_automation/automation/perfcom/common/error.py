#!/usr/bin/python3

class Error(Exception):
    pass

class APIError(Error):
    def __str__(self):
        return "Server API {} not obey the protocol".format(self.args[0])

class HTTPError(Error):
    def __str__(self):
       if len(self.args) > 1:
          msg = self.args[1]
       else:
          msg = ""
       return "{0}:{1}".format(self.args[0], msg)

class ProgrammingError(Error):
    pass

class ErrorArg(Error):
    pass

class InvalidLogError(Error):
    pass

class InvalidRunDir(Error):
    pass

class NoPlanError(Error):
    def __str__(self):
        return "No Plan".format(self.args[0])
