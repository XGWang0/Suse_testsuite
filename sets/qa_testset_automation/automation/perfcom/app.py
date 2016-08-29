#!/usr/bin/python3

import logging
logging.basicConfig(level=logging.DEBUG, datefmt='%H:%M:%S')
import sys
import argparse
from error import *
import cmd
import shlex
from common import apicall

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        raise CMDArgError()

class CmdArg:
    parser = ArgumentParser(description= "perfcom cmdline")
    parser.add_argument('-s', '--server', dest='g_server', type=str,
                        default='147.2.207.100',
                        help="the perfcom server IP")
    parser.add_argument('-p', '--port', dest='g_port', type=int,
                        nargs='?', default='8888',
                        help="the perfcom server port")
    subparsers = parser.add_subparsers(dest="subcmd")

    def usage(args):
        CmdArg.parser.print_usage(sys.stderr)

    help_parser = subparsers.add_parser("help")
    help_parser.set_defaults(func=usage)

    @classmethod
    def run(cls, cmdline):
        try:
            args = cls.parser.parse_args(cmdline)
        except CMDArgError:
            return False
        APP.init(args.g_server, args.g_port)
        if hasattr(args, "func"):
            return args.func(args)
        else:
            APP.enable_interactive()

    @classmethod
    def add_parser(cls, cmd_name):
        return cls.subparsers.add_parser(cmd_name)

class APP:
    interactive = False
    @classmethod
    def init(cls, server, port):
        cls.client = apicall.apiClient(server, port)
        cls.dynapi = apicall.dynAPI(cls.client)

    @classmethod
    def enable_interactive(cls):
        cls.interactive = True

    @classmethod
    def isinteractive(cls):
        return cls.interactive == True

    @classmethod
    def run(cls, argv):
        CmdArg.run(argv)
        if APP.interactive:
            REPL.run()

class CmdContext:
    def __init__(self, name):
        self.name = name
        self._cmd_dict = {}

    def register_cmd(self, cmd, func):
        self._cmd_dict[cmd] = func

    def resolve_cmd(self, cmd):
        try:
            return self._cmd_dict[cmd]
        except KeyError:
            return None

    def start(self):
        pass

    def end(self):
        pass

class CmdOne:
    def __init__(self, cmd_context=None):
        self.cmd_context = cmd_context

    def setup(self, parser):
        pass

    def run(self, args):
        raise NotImplementedError

class SubCmd:
    @classmethod
    def run(cls, args):
        raise NotImplementedError

    @classmethod
    def init_parser(cls, parser):
        pass

def cmd_init(cmd_name, cmd_class):
    #init_parser
    def subcmd(args):
        cmd_class.run(args)
    parser = CmdArg.add_parser(cmd_name)
    parser.set_defaults(func=subcmd)
    cmd_class.init_parser(parser)
    #init_repl
    def replcmd(args):
        try:
            args = parser.parse_args(args)
        except CMDArgError:
            return False
        return subcmd(args)
    REPL.register_cmd(cmd_name, replcmd)

def cmd_init_with_context(cmd_name, cmd_class, context):
    #If a cmd is with a context it means it is interavtive.
    #So not need to add_parser to cmdline
    def subcmd(args):
        cmd_class.run(args)
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=subcmd)
    cmd_class.init_parser(parser)
    #init_repl
    def replcmd(args):
        try:
            args = parser.parse_args(args)
        except CMDArgError:
            return False
        return subcmd(args)
    REPL.register_cmd_with_context(cmd_name, replcmd)


class CmdREPL(cmd.Cmd):
    intro = "perfcom client interactive mode"
    prompt = "perfcom > "
    top_context = CmdContext("top")
    all_contexts = {}
    context_stack = []

    def __init__(self, *args, **kargs):
        super(CmdREPL, self).__init__(*args, **kargs)
        self._cmd_dict = dict()

    def cmdline_parse(self, arg):
        return shlex.split(arg)

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF' : #end the loop
            self.lastcmd = ''
            return True
        if cmd == '':
            return self.default(line)
        else:
            func = None
            for context in reversed(self.__class__.context_stack):
                func = context.resolve_cmd(cmd)
                if not func:
                    break
            if not func:
                func = self.__class__.top_context.resolve_cmd(cmd)
            if not func:
                return self.default(line)
            args = self.cmdline_parse(arg)
            return func(args)

class REPL:
    singleton = CmdREPL()
    @classmethod
    def run(cls):
        cls.singleton.cmdloop()

    @classmethod
    def register_cmd(cls, cmd, func):
        cls.register_cmd_with_context("top", cmd, func)

    @classmethod
    def register_cmd_with_context(cls, context, cmd, func):
        if isinstance(context, CmdContext):
            context_name = context.name
            cls.singleton.all_contexts[context_name] = context
        else:
            context_name = context
            try:
                context = cls.singleton.all_contexts[context_name]
            except KeyError:
                context = CmdContext(context_name)
                cls.singleton.all_contexts[context_name] = context
        context.register_cmd(cmd, func)

    @classmethod
    def push_context(cls, context):
        if isinstance(context, CmdContext):
            context_name = context.name
            cls.singleton.all_contexts[context_name] = context
        else:
            context_name = context
            try:
                context = cls.singleton.all_contexts[context_name]
            except KeyError:
                raise ProgrammnigError("no context {}".format(context_name))
        context.start()
        cls.singleton.context_stack.append(context)

    @classmethod
    def pop_context(cls):
        try:
            context = cls.singleton.context_stack.pop()
        except IndexError:
            raise ProgrammnigError("pop empty context stack")
        context.end()

    @classmethod
    def current_context(cls):
        assert(len(cls.singleton.context_stack))
        return cls.singleton.context_stack[-1]

    @classmethod
    def set_prompt(cls, prompt):
        cls.singleton.prompt = prompt

import subcmd
