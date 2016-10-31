# __author__ = 'kuhn'
# __doc__ = "starts transformation with dgd configuration"
#
# import sys
# import os
# import processor
# import logging
# from optparse import OptionParser
# import primarylink
# import postprocessing
# import cmdiresource
#
# # if __name__ == '__main__':
# #     # logging.basicConfig(level="info")
# #     # read the configuration file from command line
# #
# #     # TODO: define options
# #     optionparse = OptionParser()
# #
# # try:
# #     configuration = processor.Configurator(sys.argv[1])
# # except IndexError:
# #     logging.error("No configuration file given. Aborting")
# #     sys.exit()
# # except IOError:
# #     logging.error("configuration File" + sys.argv[1] + " not found.")
# #     sys.exit()
#
# # set the xslt processor
# proc = processor.XSLBatchProcessor(
#     configuration.globals.get("processor"))
#
# # start the processor for corpus, event and speaker
# print "starting corpus transformations"
# proc.start(configuration.corpus.get("stylesheet"),
#            configuration.corpus.get("indirectory"),
#            configuration.corpus.get("prefix"),
#            configuration.corpus.get("outdirectory"))
# print "starting event transformations"
# proc.start(configuration.event.get("stylesheet"),
#            configuration.event.get("indirectory"),
#            configuration.event.get("prefix"),
#            configuration.event.get("outdirectory"))
# print "starting speaker transformation"
# proc.start(configuration.speaker.get("stylesheet"),
#            configuration.speaker.get("indirectory"),
#            configuration.speaker.get("prefix"),
#            configuration.speaker.get("outdirectory"))
#
# print "finished tranformations"
#
# primdat = primarylink.PrimaryDataPath('/data/primarypath.csv')
#
# # build the cmdi resource tree for referencing
# cmdi_resourcetree = cmdiresource.ResourceTreeCollection(configuration.corpus.get("outdirectory"),
#                                                         configuration.event.get("outdirectory"),
#                                                         configuration.speaker.get("outdirectory"))
#
#
#
# valueprocessor = postprocessing.ValueProcessing()
#
#
