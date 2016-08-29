#!/usr/bin/python3


class Error(Exception):
    pass

class ProgrammingError(Error):
    pass

class CMDArgError(Error):
    pass

class CMDNoSubCMDError(Error):
    pass
