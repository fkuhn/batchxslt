from __future__ import unicode_literals

import argparse
import os
import sys

from prompt_toolkit import prompt
from pygments.token import Token
from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface


# path to cmdi schema files
CMDIR = "/data/cmdi"


#defapplication = Application(
#    layout=layout,
#    key_bindings_registry=registry,

    # Let's add mouse support as well.
 #   mouse_support=True,

    # For fullscreen:
 #   use_alternate_screen=True)


def transform(dgdmetafile=None, corpusname=None, resourcetype=None):
    """

    :param dgdmetafile:
    :param corpusname:
    :param resourcetype:
    :return:
    """
    print "testing2"


def interactive():
    """
    interactive mode
    """
    #reading available schemes

    dgdfolder = prompt("Enter a ressource folder path: ")
    cmdifolder = prompt("Choose a cmdi schema")

def main():
    """
    This is the main function used for cli functionability.
    """
    interactive()

    # transform()

    # b) define a config file based transformation
    # default case w/o parameters
