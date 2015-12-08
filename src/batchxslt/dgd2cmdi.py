from __future__ import unicode_literals

import argparse
import os
import sys
import config

from prompt_toolkit import prompt
from pygments.token import Token
from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface


#default config path
CONF = os.path.abspath('/data/config/')+'config.yml'


#defapplication = Application(
#    layout=layout,
#    key_bindings_registry=registry,

    # Let's add mouse support as well.
 #   mouse_support=True,

    # For fullscreen:
 #   use_alternate_screen=True)


def main():
    """
    This is the main function used for cli functionability.
    """

    # configuration = config.load_configuration()

    parser = argparse.ArgumentParser()

    # transform()

    # b) define a config file based transformation
    # default case w/o parameters
