__author__ = 'kuhn'

import networkx
import codecs
import logging
import os
from lxml import etree
import sys

# TODO: define paths in csv files
DGDROOT = "dgd2_data"
RESOURCEPROXIES = "ResourceProxyList"
SPEAKERXPATH = "//InEvent/Event"
RESOURCEPATH = "dgd2_data/dgd2cmdi/cmdiOutput/"
PREFIX = 'cmdi_'
NAME = 'AGD'

class ResourceTreeCollection(networkx.MultiDiGraph):
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
        self.name = NAME
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

            """
            define eventnodes. note that each event has a number of sessions that
            are not explicitly stored as nodes.
            """

            if self.has_node(event):
                eventcorpusfilepath = eventspath + '/' + event

                for filename in os.listdir(eventcorpusfilepath):
                    try:
                        etr = etree.parse(eventcorpusfilepath + '/' + filename)
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning. xml file was not parsed: " +
                                      filename)
                        continue

                    eventnodename = filename.split('.')[0].lstrip(PREFIX).rstrip('_extern')
                    self.add_node(eventnodename, {
                        'repopath': self.contextpath(event, DGDROOT),
                        'corpusroot': False,
                        'type': 'metadata',
                        'etreeobject': etr,
                        'filename': filename}
                    )
                    self.add_edge(event, eventnodename)
            # finally connect an event to all speakers that take part in it.
            for speaker in self.find_speakers(event):
                self.add_edge(event, speaker)

        # define speaker nodes and add them to their corpus root

        for speakercorp in speakercorpusnames:

            """
            define speakernodes. note that each speaker is part of an session
            in an event. to just find the event, a speaker has taken part,
            access the <InEvent> element of the speaker cmdi metadata.
            """

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
                    speakernodename = filename.split('.')[0].lstrip(PREFIX).rstrip('_extern')
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

                    speakerevents = self.find_events(speakernodename)
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

    def find_eventsessions(self, speakernode):
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
        ineventsessions_out = [event.text for event in inevent]
        return ineventsessions_out

    def find_events(self, speakernode):
        """
        :param speakernode
        :return list of event labels
        searches for events a speaker takes part in by looking up the
        metadata itself.
        Since there is no physical resource for sessions, they are not
        filed as nodes.
        """
        sessions = self.find_eventsessions(speakernode)
        # take the session of event label and split it down to the event
        events = ['_'.join(str(segment) for segment in session.split('_')[0:3])
                  for session in sessions]
        events = list(set(events))
        return events

    def find_speakers(self, eventnode):
        """
        :param eventnode:
        :return: list of speaker labels fo/und in event
        """
        session = "//Session"
        speakerpath = "Speaker/Label"
        sessionsofevent = self.node.get(eventnode).get("etreeobject").xpath(session)
        speakerlabels = list()

        # add all sessions of the event as attribute
        self.node.get(eventnode).update({'sessions': sessionsofevent})

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

        cmdi_etrobj = self.node.get(metafilenode).get("etreeobject")
        cmdiroot = cmdi_etrobj.getroot()
        resourceproxies = cmdiroot.find("ResourceProxyList")

        speakers = self.find_speakers(metafilenode)
        events = self.find_events(metafilenode)
        #FIXME: resource_nodes is NoneType Object
        resource_nodes = events + speakers # todo: insert corpus reference

        for node in resource_nodes:
            # where is the edge pointed to?
            # access the filename
            node_fname = self.node.get(node).get("filename")
            resourceproxy = etree.Element("ResourceProxy")
            resourceproxy.text = str(node)
            resourceproxy.set("href", node_fname)

            # insert new resourceproxyelement in list
            resourceproxies.append(resourceproxy)
            

    def build_resourceproxy(self):
        """
        inplace resourceproxy generation of the resource.
        modifies the stored etree object of each resource.
        :param cmdifile:
        :return:
        """

        for resource in self.nodes_iter():

            # get the etreeobject
            if resource is not NoneType:
                self.define_resourceproxy(resource)

    def get_cmdi(self, nodename):
        """
        outputs the cmdi of the node as prettyprinted xml.
        :param outputpath:
        :return:
        """

        pass

    def build_geolocations(self):
        """
        inplace computation of the geolocations
        :return:
        """
        # TODO: find geolocation package to compute locations
        # from the provided grid coordinates

        for node in self.nodes_iter():

            pass






