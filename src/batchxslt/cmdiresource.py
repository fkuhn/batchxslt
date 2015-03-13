__author__ = 'kuhn'

import networkx
import codecs
import logging
import os
from lxml import etree

DGDROOT = "dgd2_data"
SPEAKERXPATH = "//InEvent/Event"


class ResourceTreeCollection(networkx.DiGraph):
    """
    represent resources in a tree structure. all involved paths
    The resurce collection is a Digraph representation of all data.
    each data is a node that holds a dict defining their attributes:

    repopath : <path locates the metadata file in the dgd repository scopus>
    corpusroot : <boolean. is the file a corpus catalogue or not?>

    input data paths must be pointed towards already cmdi transformed data.
    """

    def __init__(self, corpuspath, eventspath, speakerspath):
        super(ResourceTreeCollection, self).__init__()
        corpusnames = os.listdir(corpuspath)
        eventcorpusnames = os.listdir(eventspath)
        speakercorpusnames = os.listdir(speakerspath)
        # cwdstart = os.getcwd()

        # define a collection root that precedes all corpora
        self.add_node("AGD_root")

        if cmp(corpusnames, eventcorpusnames) and cmp(eventcorpusnames,
                                                      speakercorpusnames):
            logging.info("Resources are aligned")
            print corpusnames
            print eventcorpusnames
            print speakercorpusnames

        else:
            logging.error("Resources are not aligned. Check paths and/ or"
                          "consistency of resource subsets")

        # define corpus nodes

        for corpus in corpusnames:
            # iterate over all corpus file names in corpus metadata dir
            # and define a node for each.
            try:
                etr = etree.parse(corpuspath+'/'+corpus)
            except (etree.XMLSyntaxError, IOError):
                logging.error("Warning. xml file was not parsed: "+corpus)
                continue

            self.add_node(
                corpus.split('_')[0].rstrip('-').lstrip('CMDI_'),
                {
                    'repopath': self.contextpath(corpus, DGDROOT),
                    'corpusroot': True,
                    'type': 'metadata',
                    'etreeobject': etr}

            )
            # add edge from root to current node
            self.add_edge('AGD_root', corpus.split('_')[0].rstrip('-'))

        # define event nodes and add add them to their corpus root

        for event in eventcorpusnames:

            if self.has_node(event):
                eventcorpusfilepath = eventspath + '/' + event

                for filename in os.listdir(eventcorpusfilepath):
                    try:
                        etr = etree.parse(eventcorpusfilepath + '/' + filename)
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning. xml file was not parsed: " +
                                      filename)
                        continue

                    eventnodename = filename.split('.')[0].lstrip('CMDI_')
                    self.add_node(eventnodename, {
                        'repopath': self.contextpath(event, DGDROOT),
                        'corpusroot': False,
                        'type': 'metadata',
                        'etreeobject': etr}
                    )
                    self.add_edge(event, eventnodename)

        # define speaker nodes and add them to their corpus root

        for speakercorp in speakercorpusnames:
            # find corpus the speaker is part of
            if self.has_node(speakercorp):
                speakercorpusfilepath = speakerspath + '/' + speakercorp

                for filename in os.listdir(speakercorpusfilepath):
                    try:
                        etr = etree.parse(speakercorpusfilepath+'/' + filename)
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning. xml file was not parsed: " +
                                      filename)
                        continue
                    speakernodename = filename.split('.')[0].lstrip('CMDI_')
                    self.add_node(speakernodename, {
                        'repopath': self.contextpath(speakercorp, DGDROOT),
                        'corpusroot': False,
                        'type': 'metadata',
                        'etreeobject': etr}
                    )
                    # define an edge from the parent corpus (speakercorp)
                    # to the current speakernode
                    self.add_edge(speakercorp, speakernodename)
                    # define edges from events to current speaker
                    speakerevents = self.findevents(speakernodename)
                    for event in speakerevents:
                        self.add_edge(event, speakernodename)

    @staticmethod
    def contextpath(fname, startpath):
        # FIXME: method always returns None.
        """find the path from a startpath to a given file"""
        for root, dirs, files in os.walk(startpath):
            if fname in files:
                return os.path.join(root, fname)
            else:
                return None

    @staticmethod
    def findevents(speakernode):
        """
        :param speakernode
        :return list of event labels
        searches for events a speaker takes part in by looking up the
        metadata itself
        """
        expression = "/CMD/Components/InEvents/Event"
        inevent = speakernode.get("etreeobject").xpath(expression)

        inevent = [event.text.split('.')[0] for event in inevent]
        return inevent





