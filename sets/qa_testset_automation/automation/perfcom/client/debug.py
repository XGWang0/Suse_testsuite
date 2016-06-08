#!/use/bin/python3
import sys
import pprint

__all__ = ["devlog", "devlog_obj"]
ns = locals()

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
LIGHT_PURPLE = '\033[94m'
PURPLE = '\033[95m'
END = '\033[0m'

devlog = print

def define_color_logger(color):
    def f(s):
        print(color, end="")
        print(s)
        print(END, end="")
    return f

fname = {"devlogR": RED, "devlogG": GREEN, "devlogY": YELLOW,
         "devlogL": LIGHT_PURPLE, "devlogP":PURPLE}

for k, v in fname.items():
    ns[k] = define_color_logger(v)
    __all__.append(k)

def define_obj_logger():
    printer = pprint.PrettyPrinter()
    def f(object):
        printer.pprint(object)
    return f
devlog_obj = define_obj_logger()

def define_color_obj_logger(color):
    def f(object):
        print(color, end="")
        devlog_obj(object)
        print(END, end="")
    return f

fname = {"devlogR_obj": RED, "devlogG_obj": GREEN, "devlogY_obj": YELLOW,
         "devlogL_obj": LIGHT_PURPLE, "devlogP_obj":PURPLE}

for k, v in fname.items():
    ns[k] = define_color_obj_logger(v)
    __all__.append(k)
