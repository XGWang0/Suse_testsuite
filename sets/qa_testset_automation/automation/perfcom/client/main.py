#!/usr/bin/python3

import sys
import argparse
from . import apicall

main_parser = argparse.ArgumentParser(description= "perfcom cmdline")
main_parser.add_argument('-s', '--server', dest='g_server', type=str, help="the perfcom server IP", default='147.2.207.100')
main_parser.add_argument('-p', '--port', dest='g_port', type=int, nargs='?', help="the perfcom server port", default='8888')
sub_parsers = main_parser.add_subparsers(dest="subcmd")

def run(cmdline):
    args = main_parser.parse_args(cmdline)
    api_client = apicall.apiClient(args.g_server, args.g_port)
    args.dynapi = apicall.dynAPI(api_client)
    if not hasattr(args, "func"):
        sys.stderr.write("One subcmd needs!\n")
        main_parser.print_usage(sys.stderr)
        sys.exit(1)
    else:
        args.func(args)
