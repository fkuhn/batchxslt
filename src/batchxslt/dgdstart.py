__author__ = 'kuhn'
__doc__ = "starts transformation with dgd configuration"

import sys
import processor
import logging
from optparse import OptionParser


if __name__ == '__main__':
    logging.basicConfig(level="info")
    # read the configuration file from command line

    # define options
    optionparse = OptionParser()

try:
    configuration = processor.ConfigParser(sys.argv[1])
except IndexError:
    logging.error("No configuration file given. Aborting")
    sys.exit()
except IOError:
    logging.error("configuration File" + sys.argv[1] + " not found.")
    sys.exit()

# TODO: use a better option handling.

# set the xslt processor
proc = processor.XSLBatchProcessor(
    configuration.globals.get("processor"))

# start the processor for corpus, event and speaker
print "starting corpus transformations"
proc.start(configuration.corpus.get("stylesheet"),
           configuration.corpus.get("indirectory"),
           configuration.corpus.get("prefix"),
           configuration.corpus.get("outdirectory"))
print "starting event transformations"
proc.start(configuration.event.get("stylesheet"),
           configuration.event.get("indirectory"),
           configuration.event.get("prefix"),
           configuration.event.get("outdirectory"))
print "starting speaker transformation"
proc.start(configuration.speaker.get("stylesheet"),
           configuration.speaker.get("indirectory"),
           configuration.speaker.get("prefix"),
           configuration.speaker.get("outdirectory"))

print "finished tranformations"



