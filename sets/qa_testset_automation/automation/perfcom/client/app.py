#!/usr/bin/python3

import logging
logging.basicConfig(level=logging.DEBUG, datefmt='%H:%M:%S')
import sys
from .error import *
from . import main
from . import (cmdrun, submitlog, comparelog, comparerun, querylog)

def usage(args):
    main.main_parser.print_usage(sys.stderr)
    sys.exit(1)

help_parser = main.sub_parsers.add_parser("help")
help_parser.set_defaults(func=usage)

def run(cmdline):
    main.run(cmdline)
