"""
IPython magic for sending slack notifications.

Copyright 2017, Konstantin Tretyakov
Based on: https://github.com/kalaidin/ipytelegram/blob/master/ipytelegram.py
License: MIT
"""

import sys
import os
import slacker
import argparse
import string
from io import StringIO, BytesIO
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

class SafeFormatDict(dict):
    def __init__(self, main_dict, secondary_dict):
        super(SafeFormatDict, self).__init__(main_dict)
        self.secondary_dict = secondary_dict
    def __missing__(self, key):
        return self.secondary_dict.get(key, '{' + key + '}')

class SafeFormatList(object):
    def __getitem__(self, idx):
        return '{%d}' % idx

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
        self.slacker = None
        p = ArgumentParser()
        p.add_argument('-c', '--channel', default=None)
        p.add_argument('-u', '--as_user', default=None)
        p.add_argument('-t', '--token', default=None)
        p.add_argument('file', nargs='?', default=None)
        self.parser = p
        self._default_config()
        
    def _update_args(self, new_args):
        self.args.channel = new_args.channel or self.args.channel
        self.args.as_user = new_args.as_user or self.args.as_user
        self.args.token = new_args.token or self.args.token
        if self.args.token:
            self.slacker = slacker.Slacker(self.args.token)
    
    def _read_config_file(self, filename, strict=False):
        if strict and not os.path.exists(filename):
            raise ValueError("File %s does not exist!" % filename)
        line = '' if not os.path.exists(filename) else open(filename).readline().strip()
        self._update_args(self.parser.parse_args(line.split()))
    
    def _default_config(self):
        self.args = self.parser.parse_args([])
        self._read_config_file(os.path.expanduser('~/.ipyslack.cfg'))
        self._read_config_file('.ipyslack.cfg')
        
    @line_magic
    def slack_setup(self, line):
        args = self.parser.parse_args(line.strip().split())
        if args.file is not None:
            self._read_config_file(args.file, True)
        self._update_args(args)

    @cell_magic
    def slack_notify(self, line, cell):
        if not self.slacker or not self.args.channel: 
            self._default_config()
        if not self.slacker or not self.args.channel: 
            raise ValueError("Call %slack_setup -t <token> -c <#channel_or_@user> first or provide this information in .ipyslack.cfg.")
        with Capture('stdout') as stdout, Capture('stderr') as stderr:
            result = self.shell.run_cell(cell)
        out = stdout.data.getvalue()
        err = stderr.data.getvalue()
        exc = repr(result.error_in_exec) if result.error_in_exec else ''
        self.slacker.chat.post_message(self.args.channel, self._format_message(line), as_user=self.args.as_user)

    @line_magic
    def slack_send(self, line):
        if not self.slacker or not self.args.channel: 
            self._default_config()
        if not self.slacker or not self.args.channel: 
            raise ValueError("Call %slack_setup -t <token> -c <#channel_or_@user> first or provide this information in .ipyslack.cfg.")
        self.slacker.chat.post_message(self.args.channel, self._format_message(line), as_user=self.args.as_user)

    def _format_message(self, msg, override_ns = dict()):
        if msg == '': msg = ' '   # Slack does not like empty messages
        msg = msg.replace('\\n', '\n')
        try:
            return string.Formatter().vformat(msg, SafeFormatList(), SafeFormatDict(override_ns, self.shell.user_ns))
        except:
            return msg  # May fail if one uses weird formatting stuff, e.g. {nonexistent_var.something}
    
def load_ipython_extension(ipython):
    magics = SlackMagics(ipython)
    ipython.register_magics(magics)

def unload_ipython_extension(ipython):
    pass