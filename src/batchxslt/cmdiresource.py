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
        cwdStart = os.getcwd()

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
                corpus.split('_')[0].rstrip('-'),
                {
                    'repopath': self.contextpath(corpus, DGDROOT),
                    'corpusroot': True,
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

                    eventnodename = filename.split('.')[0]
                    self.add_node(eventnodename, {
                        'repopath': self.contextpath(event, DGDROOT),
                        'corpusroot': False,
                        'etreeobject': etr}
                    )
                    self.add_edge(event, eventnodename)

        # define speaker nodes and add them to their corpus root

        # change cwd to events directory

        for speaker in speakercorpusnames:

            if self.has_node(speaker):
                speakercorpusfilepath = speakerspath + '/' + speaker

                for filename in os.listdir(speakercorpusfilepath):
                    try:
                        etr = etree.parse(speakercorpusfilepath+'/' + filename)
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning. xml file was not parsed: " +
                                      filename)
                        continue
                    speakernodename = filename.split('.')[0]
                    self.add_node(speakernodename, {
                        'repopath': self.contextpath(speaker, DGDROOT),
                        'corpusroot': False,
                        'etreeobject': etr}
                    )
                    self.add_edge(speaker, speakernodename)

        # TODO: add event ->speaker edges for speaker in events



    @staticmethod
    def contextpath(fname, startpath):
        # FIXME: method always returns None.
        """find the path from a startpath to a given file"""
        for root, dirs, files in os.walk(startpath):
            if fname in files:
                return os.path.join(root, fname)
            else:
                return None

    # TODO: find all speakers in an event

    @staticmethod
    def findevents(speakernode):
        """
        :param speakernode
        :return list of event labels
        searches for events a speaker takes part in by looking up the
        metadata itself with xpath
        """

        root = speakernode.get("etreeobject").getroot()


class ResourceTree(networkx.DiGraph):
    """
    a b-tree structure to link all local dgd resources, generated for
    each dgd metadata file.
    Starting point: ResourceBTree is a child of networkx.DiGraph
    """

    # TODO: Find a packages for tree representation or use networx

    def __init__(self, filename):
        super(ResourceTree).__init__()
        """
        init a resource tree object as directed graph:
        read in a cmdi-transformed dgd metafile
        :return:
        """
        self.etreeobject = None
        try:
            self.etreeobject = etree.parse(codecs.open(filename,
                                                       encoding="utf-8"))

        except IOError:
            logging.error("file not readable")

        fileroot = self.etreeobject.getroot()

        for element in fileroot.iter():
            print




