# Example package with a console entry point
__author__ = "fkuhn"
__doc__ = "batchxslt 0.1 Refer to /doc for a tutorial."

import processor
import logging
import sys


def main():
    """
    console entry point
    """
    print "batchxslt 0.2"

    try:
        configuration = processor.Configurator(sys.argv[1])
    except IndexError:
        logging.error("No configuration file given. Aborting")
        sys.exit()
    except IOError:
        logging.error("configuration File" + sys.argv[1] + " not found.")
        sys.exit()


