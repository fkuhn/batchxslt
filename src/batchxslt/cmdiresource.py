__author__ = 'kuhn'

import networkx
import codecs
import logging
import os
from lxml import etree
import sys
import mimetypes

# TODO: define paths in csv files
DGDROOT = "dgd2_data"
RESOURCEPROXIES = "ResourceProxyList"
SPEAKERXPATH = "//InEvent/Event"
RESOURCEPATH = "dgd2_data/dgd2cmdi/cmdiOutput/"
PREFIX = 'cmdi_'
NAME = 'AGD'

import urllib

# this is the landing page prefix for the agd werbservice
LANDINGPG = u"http://dgd.ids-mannheim.de/service/DGD2Web/ExternalAccessServlet?command=displayData&id="

class ResourceTreeCollection(networkx.MultiDiGraph):
    """
    represent resources in a tree structure. all involved paths
    The resurce collection is a Digraph representation of all data.
    each data is a node that holds a dict defining their attributes:

    repopath : <path locates the metadata file in the dgd repository scopus>
    corpusroot : <boolean. is the file a corpus catalogue or not?>

    input data paths must be pointed towards already cmdi transformed data.

    NOTE: April 29th
    Speakers are not removed from resource proxy generation. Transcript nodes
    are added. their type is labelled "transcript" accordingly.

    """

    def __init__(self, corpuspath, eventspath, speakerspath, transcriptspath):
        super(ResourceTreeCollection, self).__init__()
        corpusnames = os.listdir(corpuspath)
        eventcorpusnames = os.listdir(eventspath)
        speakercorpusnames = os.listdir(speakerspath)
        transcriptscorpusnames = os.listdir(transcriptspath)
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

        # define transcriptnodes and add them to their corpusroot

        for transcriptcorp in transcriptscorpusnames:

            """
            define transcriptnodes for each corpus found in the primary source folders
            the event that an trancript is counted to is simply derived by splitting the
            string of the transcript filename. naming paradigm will not change so method is
            simple and safe.
            Each transcript is part of a recording session.
            """

            if self.has_node(transcriptcorp):

                transcriptcorpusfilepath = transcriptspath + '/' + transcriptcorp

                for filename in os.listdir(transcriptcorpusfilepath):

                    # contruct node name. eg. from FOLK_E_00004_SE_01_T_01_DF_01.fln
                    transcriptnodename = filename.split('.')[0]

                    self.add_node(transcriptnodename, {
                        'repopath': transcriptcorp,
                        'corpusroot': False,
                        'type': 'transcript',
                        'etreeobject': None,
                        'filename': filename}
                    )

                    # obtain event from filename
                    transcriptevent = '_'.join(transcriptnodename.split('_')[:3])
                    # define edge from event to transcript
                    self.add_edge(transcriptevent, transcriptnodename)

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

    def find_transcripts(self, eventnode):
        """
        finds trancripts associated with given event
        :param eventnode:
        :return:
        """
        transcripts = list()
        for nodename in eventnode.out_edges():
            if self.node.get(nodename).get('type') == 'transcript':
                transcripts.append(nodename)

        return transcripts


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
        resourceproxies = cmdiroot.find("Resources").find("ResourceProxyList")

        in_nodes = [i[0] for i in self.in_edges(metafilenode)]
        out_nodes = [i[1] for i in self.out_edges(metafilenode)]



        resource_nodes = out_nodes + in_nodes

        # remove speaker references for now
        for speaker in self.find_speakers(metafilenode):
            if speaker in resource_nodes:
                resource_nodes.remove(speaker)

        # remove the abstract node from the resource list
        if 'AGD_root' in resource_nodes:
            resource_nodes.remove('AGD_root')
        if metafilenode in resource_nodes:
            resource_nodes.remove(metafilenode)
        # make sure there are just unique references
        resource_nodes = set(resource_nodes)

        for node in resource_nodes:
            # where is the edge pointed to?
            # access the filename

            node_fname = self.node.get(node).get("filename")
            resourceproxy = etree.SubElement(resourceproxies, "ResourceProxy")
            resourceref = etree.SubElement(resourceproxy, "ResourceRef")
            resourcetype = etree.SubElement(resourceproxy, "ResourceType")
            resourceproxy.set("id", node)

            resourcetype.set("mimetype", str(mimetypes.guess_type(node_fname)[0]))
            landingpage = urllib.unquote(LANDINGPG)
            resourceref.text = node
            resourceref.set("href", landingpage + node)

            # Generate an is PartRelationship for backreference
            ispart = etree.SubElement(resourceproxy, "ResourceIsPart")


            # insert new resourceproxyelement in list
            # resourceproxies.append(resourceproxy)

        # version resource info
        # isVersionOf = etree.SubElement(resourceproxies, "isVersionOf")

    def write_xml(self, nodename, fname):
        """
        write the xml of a node
        :param node:
        :return:
        """
        self.node.get(nodename).get('etreeobject').write(fname, encoding='utf-8', method='xml')

    def build_resourceproxy(self):
        """
        inplace resourceproxy generation of the resource.
        modifies the stored etree object of each resource.
        :param cmdifile:
        :return:
        """

        for resource in self.nodes_iter():

            # pass the node name to define_resourceproxy
            if resource != 'AGD_root':
                self.define_resourceproxy(resource)
            # exclude transcript nodes since they have no metadata
            elif self.node.get(resource).get('type') != 'transcript':
                self.define_resourceproxy(resource)

    def get_cmdi(self, nodename):
        """
        outputs the cmdi of the node as prettyprinted xml.
        :param outputpath:
        :return:
        """

        pass

    def build_geolocation(self, nodename):
        """
        inplace computation of the geolocations
        :return:
        """
        # TODO: find geolocation package to compute locations
        # from the provided grid coordinates
        
        # if provided, obtain grid coordinates.

        for node in self.nodes_iter():

            pass






