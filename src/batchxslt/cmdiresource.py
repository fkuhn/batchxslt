__author__ = 'kuhn'

import networkx
import codecs
import logging
import os
from lxml import etree

# TODO: define paths in csv files
DGDROOT = "dgd2_data"
RESOURCEPROXIES = "ResourceProxyList"
SPEAKERXPATH = "//InEvent/Event"
RESOURCEPATH = "dgd2_data/dgd2cmdi/cmdiOutput/"


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
                corpus.split('_')[1].rstrip('-'),
                {
                    'repopath': self.contextpath(corpus, DGDROOT),
                    'corpusroot': True,
                    'type': 'metadata',
                    'etreeobject': etr,
                    'filename': corpus}

            )
            # add edge from root to current node
            self.add_edge('AGD_root', corpus.split('_')[1].rstrip('-'))

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
                        'etreeobject': etr,
                        'filename': filename}
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
                        'etreeobject': etr,
                        'filename': filename}
                    )
                    # define an edge from the parent corpus (speakercorp)
                    # to the current speakernode
                    # example: "PF" --> "PF--_S_00103.xml"
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

    def findevents(self, speakernode):
        """
        :param speakernode
        :return list of event labels
        searches for events a speaker takes part in by looking up the
        metadata itself.
        Since there is no physical resource for sessions, they are not
        filed as nodes.
        """
        expression = "//InEvents/EventSession"
        inevent = self.node.get(speakernode).get("etreeobject").xpath(expression)
        # must add _extern label to find in graph
        # inevent_out = [event.text + '_extern.xml' for event in inevent]
        inevent_out = [event.text for event in inevent]
        return inevent_out

    def findspeakers(self, eventnode):
        """
        :param eventnode:
        :return: list of speaker labels fo/und in event
        """
        session = "//Session"
        speakerpath = "Speaker/Label"
        sessionsofevent = self.node.get(eventnode).get("etreeobject").xpath(session)
        speakerlabels = list()

        # add all sessions of the event as attribute
        self.node(eventnode).update({'sessions': sessionsofevent})

        for session in sessionsofevent:
            # must add "_extern" label to find speaker in graphh
            speakerlabels.extend([speaker.text for speaker in session.xpath(speakerpath)])
            # speakerlabels.extend([speaker.text + '_extern.xml' for speaker in session.xpath(speakerpath)])
        return speakerlabels

    def define_resourceproxy(self, metafilenode):
        """
        defines the ResourceProxies for all Resources referred via edges
               <Resources>
        <ResourceProxyList> </ResourceProxyList>
        <JournalFileProxyList> </JournalFileProxyList>
        <ResourceRelationList> </ResourceRelationList>
        </Resources>
        :param metafilenode:
        :return:
        """

        cmdi_etrobj = metafilenode.node.get("etreeobject")
        cmdiroot = cmdi_etrobj.getroot()
        resourceproxies = cmdiroot.find("ResourceProxyList")

        out_edges = self.out_edges(metafilenode)
        for edge in out_edges:
            # where is the edge pointed to?
            node = edge[1]
            # access the filename
            node_fname = self.node.get(node).get("filename")
            resourceproxy = etree.Element("ResourceProxy")
            resourceproxy.text = node_fname
            resourceproxy.set("href", node_fname)

            # insert new resourceproxyelement in list
            resourceproxies.append(resourceproxy)
            # TODO: connect this method to the workflow
            # TODO: make sure elements are written to output



