"""
IPython magic for sending slack notifications.

Copyright 2017, Konstantin Tretyakov
Based on: https://github.com/kalaidin/ipytelegram/blob/master/ipytelegram.py
License: MIT
"""

import sys
import slacker
import argparse
from io import StringIO, BytesIO
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

class Capture(object):
    def __init__(self, name):
        self.name = name
        self.data = StringIO() if sys.version_info.major == 3 else BytesIO()
    def __enter__(self):
        self.original = getattr(sys, self.name)
        setattr(sys, self.name, self)
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        setattr(sys, self.name, self.original)
    def write(self, data):
        self.data.write(data)
        self.original.write(data)
    def flush(self):
        self.original.flush()

@magics_class
class SlackMagics(Magics):
    def __init__(self, shell):
        super(SlackMagics, self).__init__(shell)
        self.args = None
        self.slacker = None
        p = ArgumentParser()
        p.add_argument('-c', '--channel', default=None)
        p.add_argument('-u', '--as_user', action='store_true')
        p.add_argument('-t', '--token', default=None)
        self.parser = p
    
    @line_magic
    def slack_setup(self, line):
        self.args = self.parser.parse_args(line.strip().split())
        if self.args.token:
            self.slacker = slacker.Slacker(self.args.token)

    @cell_magic
    def slack_notify(self, line, cell):
        if not self.slacker or not self.args.channel: 
            raise ValueError("Call %slack_setup -t <token> -c <#channel_or_@user> first.")
        with Capture('stdout') as stdout, Capture('stderr') as stderr:
            result = self.shell.run_cell(cell)
        out = stdout.data.getvalue()
        err = stderr.data.getvalue()
        exc = repr(result.error_in_exec) if result.error_in_exec else ''
        msg = line.replace('\\n', '\n').format(out=out, err=err, exc=exc)
        if msg == '': msg = ' '
        self.slacker.chat.post_message(self.args.channel, msg, as_user=self.args.as_user)


    @line_magic
    def slack_send(self, line):
        if not self.slacker or not self.args.channel: 
            raise ValueError("Call %slack_setup -t <token> -c <#channel_or_@user> first.")
        if line == '': line = ' '
        self.slacker.chat.post_message(self.args.channel, line.replace('\\n', '\n'), as_user=self.args.as_user)

def load_ipython_extension(ipython):
    magics = SlackMagics(ipython)
    ipython.register_magics(magics)

def unload_ipython_extension(ipython):
    pass