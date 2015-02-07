__author__ = 'kuhn'

"""
starts transformation with dgd configuration.
"""

import processorClasses
import sys

# read the configuration file from command line
configuration = processorClasses.ConfigParser(sys.argv[1])

# set the xslt processor
processor = processorClasses.XSLBatchProcessor(configuration.globals.get("processor"))

# start the processor for corpus, event and speaker
print "starting corpus transformations"
processor.start(configuration.corpus.get("stylesheet"),
                 configuration.corpus.get("indirectory"),
                 configuration.corpus.get("prefix"),
                 configuration.corpus.get("outdirectory"))
print "starting event transformations"
processor.start(configuration.event.get("stylesheet"),
                 configuration.event.get("indirectory"),
                 configuration.event.get("prefix"),
                 configuration.event.get("outdirectory"))
print "starting speaker transformation"
processor.start(configuration.speaker.get("stylesheet"),
                configuration.speaker.get("indirectory"),
                configuration.speaker.get("prefix"),
                configuration.speaker.get("outdirectory"))

print "finished tranformations"

