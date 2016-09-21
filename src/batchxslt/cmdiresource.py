import logging
import mimetypes
import os
import re
import cmdiheader
import networkx
from lxml import etree

# define constants
DGDROOT = "dgd2_data"
RESOURCEPROXIES = "ResourceProxyList"
SPEAKERXPATH = "//InEvent/Event"
RESOURCEPATH = "dgd2_data/dgd2cmdi/cmdiOutput/"
PREFIX = 'cmdi_'
PREF = 'agd_ids_'
NAME = 'AGD'
SVNROOT = u'dgd2_data/dgd2cmdi/cmdi/'

# this is the landing page prefix for the agd werbservice
LANDINGPG = u'http://dgd.ids-mannheim.de/service/DGD2Web/ExternalAccessServlet?command=displayData&id='
EXTENSION = '_extern.cmdi'


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

    CMDI references only work with new transformed data (revision including
    session to event metadata)
    """

    def __init__(self, corpuspath, eventspath, speakerspath, transcriptspath):

        super(ResourceTreeCollection, self).__init__()
        corpusnames = os.listdir(os.path.abspath(corpuspath))
        eventcorpusdirectories = os.listdir(os.path.abspath(eventspath))
        speakercorpusdirectories = os.listdir(os.path.abspath(speakerspath))
        transcriptcorpusdirectories = os.listdir(os.path.abspath(transcriptspath))

        self.corpuspath = corpuspath
        self.eventspath = eventspath
        self.speakerspath = speakerspath
        self.transcriptspath = transcriptspath

        if len(corpusnames) == 0:
            print "Warning: Corpus catalogues not parsed"
        elif len(eventcorpusdirectories) == 0:
            print "Warning: Event directories not parsed"
        elif len(speakercorpusdirectories) == 0:
            print "Warning: Speaker directories not parsed"

        if len(corpusnames) != len(eventcorpusdirectories)\
                and len(corpusnames) != len(speakercorpusdirectories):
            print "Warning: initialized numbers of directories is not even"


        self.name = NAME



        # eventcorpustuples are a collection of tuples
        # with a event corpus directory and its corresponding
        # corpus label (e.g. 'PF--')
        self.eventcorpustuples = list()
        for evecorp in eventcorpusdirectories:
            for corplabel in corpusnames:
                # if a corpuslabel has len 4 and is not using
                # '-', the split command does not change anything.
                if evecorp == corplabel.rstrip(EXTENSION).split('-')[0]:
                    print "Found event directory for: {}".format(str(evecorp))
                    self.eventcorpustuples.append((evecorp,
                                                   corplabel.rstrip(EXTENSION)))
        self.speakercorpustuples = list()
        for speakcorp in speakercorpusdirectories:
            for corplabel in corpusnames:
                if speakcorp == corplabel.rstrip(EXTENSION).split('-')[0]:
                    self.speakercorpustuples.append((speakcorp,
                                                   corplabel.rstrip(EXTENSION)))

        self.transcriptcorpustuples = list()
        for transcorp in transcriptcorpusdirectories:
            for corplabel in corpusnames:
                if transcorp == corplabel.rstrip(EXTENSION).split('-')[0]:
                    self.transcriptcorpustuples.append((transcorp,
                                                     corplabel.rstrip(EXTENSION)))


        # define a collection root that precedes all corpora
        self.add_node("AGD_root")
        for corpus in corpusnames:
            # iterate over all corpus file names in corpus metadata dir
            # and define a node for each.
            try:
                etr = etree.parse(os.path.abspath(os.path.join(corpuspath, corpus)))
            except (etree.XMLSyntaxError, IOError):
                logging.error("Warning corpus xml file was not parsed: " + corpus)
                continue
            self.add_node(
                corpus.rstrip(EXTENSION),
                # corpus.split('-')[0].rstrip(EXTENSION),

                {
                    'repopath': self.contextpath(corpus, DGDROOT),
                    # 'corpus': corpus.split('-')[0].rstrip(EXTENSION),
                    'corpus': corpus.rstrip(EXTENSION),
                    'corpusroot': True,
                    'type': 'corpus',
                    'etreeobject': etr,
                    'filename': corpus,
                    'id': PREF + corpus.rstrip(EXTENSION)})
                    # 'id':  PREF + corpus.split('-')[0].rstrip(EXTENSION)})

            # add edge from root to current node
            self.add_edge('AGD_root', corpus.rstrip(EXTENSION))
            # self.add_edge('AGD_root', corpus.split('-')[0].rstrip(EXTENSION))
        # define event nodes and add add them to their corpus root

        for eventcorpustuple in self.eventcorpustuples:
            """
            define eventnodes. note that each event has a number of sessions that
            are not explicitly stored as nodes.
            """

            if self.has_node(eventcorpustuple[1]):
                # reconstruct the path to the event. must add the corpus directory
                # the corpus directory does NOT use the '-' in its name

                eventcorpusfilepath = os.path.abspath(
                    os.path.join(eventspath,
                                 eventcorpustuple[0]))

                for filename in os.listdir(eventcorpusfilepath):
                    try:
                        etr = etree.parse(os.path.join(eventcorpusfilepath, filename))
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning event file of a corpus was not parsed: " +
                                      os.path.join(eventcorpusfilepath, filename))
                        continue

                    eventnodename = filename.rstrip('_extern.cmdi')
                    self.add_node(eventnodename, {
                        'repopath': self.contextpath(eventcorpustuple[0], DGDROOT),
                        'corpus': eventcorpustuple[1],
                        'corpusroot': False,
                        'type': 'event',
                        'etreeobject': etr,
                        'filename': filename,
                        # 'id': PREF + eventcorpusname.split('-')[0].rstrip(EXTENSION)})
                        'id': PREF + eventcorpustuple[1]})
                    self.add_edge(eventcorpustuple[1], eventnodename)
                    # self.__idcount += 1
                    # find media file reference in the event
                    self.find_media(eventnodename)
                # print("Finished reading of {}".format(eventcorpusfilepath))

                # finally connect an event to all speakers that take part in it.
                # FIXME: referred before assignment: UnboundLocalError
                    try:
                        for speaker in self.find_speakers(eventnodename):
                            self.add_edge(eventnodename, speaker)
                    except UnboundLocalError:
                        continue
        for transcripttuple in self.transcriptcorpustuples:
            """
            define transcriptnodes for each corpus found in the primary source folders
            the event that an trancript is counted to is simply derived by splitting the
            string of the transcript filename. naming paradigm will not change so method is
            simple and safe.
            Each transcript is part of a recording session.
            """
            if self.has_node(transcripttuple[1]):
                transcriptcorpusfilepath = os.path.abspath(os.path.join(transcriptspath, transcripttuple[0]))
                for filename in os.listdir(transcriptcorpusfilepath):
                    # contruct node name. eg. from FOLK_E_00004_SE_01_T_01_DF_01.fln
                    transcriptnodename = filename.split('.')[0]
                    self.add_node(transcriptnodename, {
                        'repopath': transcriptcorpusfilepath +'/'+ transcriptnodename,
                        'corpus' : transcripttuple[1],
                        'corpusroot': False,
                        'type': 'transcript',
                        'etreeobject': False,
                        'filename': filename,
                        'id':  PREF + transcripttuple[1]})

                    # obtain event from filename
                    transcriptevent = '_'.join(transcriptnodename.split('_')[:3])
                    # define edge from event to transcript
                    if self.has_node(transcriptevent):
                        self.add_edge(transcriptevent, transcriptnodename)
                    # define an edge to refer from the corpus catalogue to the transcript
                    # if self.has_node(transcripttuple):
                    #     self.add_edge(transcripttuple, transcriptnodename)
        for speakertuple in self.speakercorpustuples:
            """
            define speakernodes. note that each speaker is part of an session
            in an event. to just find the event, a speaker has taken part,
            access the <InEvent> element of the speaker cmdi metadata.
            """
            # find corpus the speaker is part of
            if self.has_node(speakertuple[1]):
                speakercorpusfilepath = os.path.join(speakerspath, speakertuple[0])

                for filename in os.listdir(speakercorpusfilepath):
                    try:
                        etr = etree.parse(os.path.abspath(os.path.join(speakercorpusfilepath, filename)))
                    except (etree.XMLSyntaxError, IOError):
                        logging.error("Warning. xml file was not parsed: " +
                                      filename)
                        continue
                    speakernodename = filename.rstrip('_extern.cmdi')
                    self.add_node(speakernodename, {
                        'repopath': self.contextpath(speakertuple, DGDROOT),
                        'corpus': speakertuple[1],
                        'corpusroot': False,
                        'type': 'speaker',
                        'etreeobject': etr,
                        'filename': filename,
                        'id':  PREF + speakertuple[1]})
                    # self.__idcount += 1
                    # define an edge from the parent corpus (speakercorp)
                    # to the current speakernode
                    # example: "PF" --> "PF--_S_00103.xml"
                    self.add_edge(speakertuple[1], speakernodename)
                    # define edges from events to current speaker
                    speakerevents = self.find_events(speakernodename)
                    for event in speakerevents:
                        if self.has_node(event):
                            self.add_edge(event, speakernodename)

        # finally connect an event to all speakers that take part in it.
        for nodename, nodedata in self.nodes_iter(data=True):
            if nodedata.get('type') == 'event':
                for speaker in self.find_speakers(nodename):
                    self.add_edge(nodename, speaker)
                    #TODO: call speaker2event while initializing
                    # self.speaker2event(speaker)
            # elif nodedata.get('type') == 'speaker':
            #     for event in self.find_events(nodename):
            #         if self.has_node(event):
            #             self.add_edge(event, nodename)



    def find_media(self, resource):
        """
        adds a node and edge from event to media. for all media found in a resource node.
        :param resource:
        :return:
        """
        audiolabels = self.node.get(resource).get(
            'etreeobject').xpath('//AudioData/FileName/text()')

        for audiofile in audiolabels:
            self.add_node(audiofile.split('.')[0], {
                'repopath': self.contextpath(resource, DGDROOT),
                'corpusroot': False,
                'type': 'audio',
                'etreeobject': False,
                'filename': audiofile,
                'id':  PREF + audiofile.rstrip(EXTENSION)})

            self.add_edge(resource, audiofile.split('.')[0])

    @staticmethod
    def contextpath(fname, startpath):
        # FIXME: method always returns None.
        """find the path from a startpath to a given file"""
        for root, dirs, files in os.walk(startpath):
            if fname in files:
                return os.path.join(root, fname)
            else:
                return None

    def show_empty_etree(self):
        """
        returns all empty etree attributes for debugging
        :return:
        """
        empties = list()
        for nodename in self.nodes_iter():
            if self.node.get(nodename).get('etreeobject') is None:
                empties.append((nodename, self.node.get(nodename).get('filename')))
        return empties

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
        searches for events a speaker takes part in.
        """

        eventlist = list()
        # print "events for "+speakernode+": "
        for outedge in self.in_edges_iter([speakernode]):
            # print outedge
            try:
                if self.node.get(outedge[0]).get('type') == 'event':
                    eventlist.append(outedge[0])
            except IndexError:
                logging.error('Index Error while splitting filename: '
                              + outedge[0] + ' while accessing inedges for: ' + speakernode)

        # make sure there are unique elements in this list
        tmpset = set(eventlist)
        eventlist = list(tmpset)

        return eventlist

        # sessions = self.find_eventsessions(speakernode)
        # # take the session of event label and split it down to the event
        # events = ['_'.join(str(segment) for segment in session.split('_')[0:3])
        #           for session in sessions]
        # events = list(set(events))
        # return events

    def find_speakers(self, eventnode):
        """
        returns all speaker nodes connected to the eventnode.
        :param eventnode:
        :return: list of speaker labels fo/und in event
        """
        speakerlist = self.node.get(eventnode).get("etreeobject").\
            getroot().xpath('//Speaker/Label/text()')

        return speakerlist

        # simple split label solution
        # for outedge in self.out_edges_iter([eventnode]):
        #
        #     try:
        #         if self.node.get(outedge[1]).get('type') == 'speaker':
        #             speakerlist.append(outedge[1])
        #     except IndexError:
        #         logging.error('Index Error while splitting filename: '
        #                       + outedge[1] + ' while accessing outedges for: ' + eventnode)
        # xpath solution

        # session = "//Session"
        # speakerpath = "Speaker/Label"

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

    def get_speaker_data(self, speakernode):
        """
        returns a dict of all relevant speaker data from a metafile
        key is element.tag, value is string of the complete element
        :param speakernode:
        :return:
        """
        speakerdata = dict()

        speakerelements = self.node.get(speakernode).\
            get('etreeobject').getroot().find('Components')


        for element in speakerelements.iter():

            speakerdata.update({element.tag: etree.tostring(element)})

        return speakerdata

    def speaker2event(self, speakernode):
        """
        takes a speaker node, finds all events the speaker takes part in and writes
        the important data to the <Speaker> element of an event datum.
        :param speakernode:
        :return:
        """
        sdata = self.get_speaker_data(speakernode)

        if len(sdata) == 0:
            print "sdata is empty"

        speakertuple_complete = ('','','')

        for event in self.find_events(speakernode):

            eventtree = self.node.get(event).get('etreeobject')
            # Abbruchbedingung setzen

            # TODO: go for each session rather than each speaker

            for event_speaker in eventtree.getroot().xpath('//Speaker'):
                # write from xml string to the element (cannot pass an etree-element to another
                # document scope
                # print event_speaker.find('Label').text + ' vs ' + speakernode
                if event_speaker.find('Label').text == speakernode:

                    # prevent multiple entries to the speaker element
                    speakertuple_temp = (speakernode, event_speaker, event)

                    if speakertuple_temp == speakertuple_complete:
                         continue
                    else:
                         speakertuple_complete = speakertuple_temp

                    # get a copy of the 'Language' to insert it to 'LanguageData' below
                    languages = event_speaker.xpath('//Language')
                    for language in event_speaker.xpath('//Language'):
                        language.getparent().remove(language)

                    event_speaker.append(etree.fromstring(sdata.get('Name')))
                    event_speaker.append(etree.fromstring(sdata.get('Alias')))
                    # etree.SubElement(event_speaker, speaker_sex)
                    event_speaker.append(etree.fromstring(sdata.get('DateOfBirth')))
                    event_speaker.append(etree.fromstring(sdata.get('Education')))
                    event_speaker.append(etree.fromstring(sdata.get('Profession')))
                    event_speaker.append(etree.fromstring(sdata.get('Ethnicity')))
                    event_speaker.append(etree.fromstring(sdata.get('Nationality')))
                    event_speaker.append(etree.fromstring(sdata.get('LocationData')))
                    event_speaker.append(etree.fromstring(sdata.get('LanguageData')))
                    # deal with language data duplicates
                    # put a copy into <LanguageData> and remove it
                    language_data = event_speaker.find('LanguageData')
                    for lang in languages:
                        if lang.text in [l.text for l in language_data.xpath('Language')]:
                            # extra_lang = etree.SubElement(language_data, 'Language')
                            # extra_lang.text = lang.text
                            continue
                        else:
                            extra_lang = etree.SubElement(language_data, 'Language')
                            extra_lang.text = lang.text

    def speaker2event_session(self, speakernode):
        """
        This is a refined version of speaker2event which iterates over every session
        found in an event rather than looping over all speaker regardless of the
        session.
        takes a speaker node, finds all events the speaker takes part in and writes
        the important data to the <Speaker> element of an event-session datum.
        :param speakernode:
        :return:
        """
        sdata = self.get_speaker_data(speakernode)

        if len(sdata) == 0:
            print "sdata is empty"

        speakertuple_complete = ('', '', '')

        for event in self.find_events(speakernode):

            eventtree = self.node.get(event).get('etreeobject')
            # Abbruchbedingung setzen

            # TODO: go for each session rather than each speaker

            for event_speaker in eventtree.getroot().xpath('//Speaker'):
                # write from xml string to the element (cannot pass an etree-element to another
                # document scope
                # print event_speaker.find('Label').text + ' vs ' + speakernode
                if event_speaker.find('Label').text == speakernode:

                    # prevent multiple entries to the speaker element
                    speakertuple_temp = (speakernode, event_speaker, event)

                    if speakertuple_temp == speakertuple_complete:
                        continue
                    else:
                        speakertuple_complete = speakertuple_temp

                    # get a copy of the 'Language' to insert it to 'LanguageData' below
                    languages = event_speaker.xpath('//Language')
                    for language in event_speaker.xpath('//Language'):
                        language.getparent().remove(language)

                    event_speaker.append(etree.fromstring(sdata.get('Name')))
                    event_speaker.append(etree.fromstring(sdata.get('Alias')))
                    # etree.SubElement(event_speaker, speaker_sex)
                    event_speaker.append(etree.fromstring(sdata.get('DateOfBirth')))
                    event_speaker.append(etree.fromstring(sdata.get('Education')))
                    event_speaker.append(etree.fromstring(sdata.get('Profession')))
                    event_speaker.append(etree.fromstring(sdata.get('Ethnicity')))
                    event_speaker.append(etree.fromstring(sdata.get('Nationality')))
                    event_speaker.append(etree.fromstring(sdata.get('LocationData')))
                    event_speaker.append(etree.fromstring(sdata.get('LanguageData')))
                    # deal with language data duplicates
                    # put a copy into <LanguageData> and remove it
                    language_data = event_speaker.find('LanguageData')
                    for lang in languages:
                        if lang.text in [l.text for l in language_data.xpath('Language')]:
                            # extra_lang = etree.SubElement(language_data, 'Language')
                            # extra_lang.text = lang.text
                            continue
                        else:
                            extra_lang = etree.SubElement(language_data, 'Language')
                            extra_lang.text = lang.text

    def define_resourceproxy(self, metafilenode):
        """
        defines the ResourceProxies for all Resources referred via edges

        Resources element structure in a cmdi file.
        <Resources>
        <ResourceProxyList> </ResourceProxyList>
        <JournalFileProxyList> </JournalFileProxyList>
        <ResourceRelationList> </ResourceRelationList>
        </Resources>


        :param metafilenode:
        :return:
        """
        # define an id counter
        ID = 0
        PREF = 'agd_ids_'
        # mimetypes
        mimetypes.add_type('application/xml', '.fln')
        mimetypes.add_type('application/x-cmdi+xml', '.cmdi')
        cmdi_etrobj = self.node.get(metafilenode).get("etreeobject")
        try:
            cmdiroot = cmdi_etrobj.getroot()
        except AttributeError:
            logging.error('no root found for: ' + metafilenode)
            return

        try:
            resourceproxies = cmdiroot.find("Resources").find("ResourceProxyList")
        except AttributeError:
            logging.error("No Resource Element found in " +
                          metafilenode + ". Check cmdi file consistency.")
            return

        in_nodes = [i[0] for i in self.in_edges(metafilenode)]
        out_nodes = [i[1] for i in self.out_edges(metafilenode)]

        resource_nodes = out_nodes + in_nodes

        # remove speaker references
        for speaker in resource_nodes:
            if self.node.get(speaker).get('type') == 'speaker':
                resource_nodes.remove(speaker)
        # remove corpus reference in edges
        for nodename in resource_nodes:
            if self.node.get(nodename).get('type') == 'corpus':
                resource_nodes.remove(nodename)

        # remove the abstract node from the resource list
        if 'AGD_root' in resource_nodes:
            resource_nodes.remove('AGD_root')
        # remove self reference
        if metafilenode in resource_nodes:
            resource_nodes.remove(metafilenode)
        # make sure there are just unique references
        resource_nodes = set(resource_nodes)

        # build proxy for original metadata as "Resource"
        for node in resource_nodes:
            # define the transcripts and audio resources
            if self.node.get(node).get('type') in ['transcript', 'audio']:
                self.set_resourceproxy(node, resourceproxies,
                                       rtype='Resource')
            # define the cmdi metadate entry: just events are listed
            elif self.node.get(node).get('type') in ['event']:
                self.set_resourceproxy(node, resourceproxies,
                                       rtype='Metadata', mtype='application/x-cmdi+xml', idprefix='cmdi_',
                                       refprefix=SVNROOT+self.node.get(node).get('corpus')+'/', refpostfix='.cmdi')
                # self.set_resourceproxy(node, resourceproxies,
                #                       rtype='Resource',
                #                       refprefix=LANDINGPG, refpostfix='')

        # finally. define a proxy referring to the original metadata of the current cmdi record
        # example: for PF.cmdi this is PF--_extern.xml.
        self.set_resourceproxy(metafilenode, resourceproxies, rtype='Resource')

    def set_resourceproxy(self, nodename, resourceproxies,
                          rtype='Metadata', mtype=None, idprefix='',
                          refprefix=LANDINGPG, refpostfix=''):
        """
        sets a resourceproxy entry and its subelements.
        :param nodename:
        :param resourceproxies:
        :return:
        """
        if mtype is None:
            node_fname = self.node.get(nodename).get("filename")
            mtype = str(mimetypes.guess_type(node_fname)[0])

        resource_proxy = etree.SubElement(resourceproxies, "ResourceProxy")
        resource_type = etree.SubElement(resource_proxy, "ResourceType")
        resource_ref = etree.SubElement(resource_proxy, "ResourceRef")
        resource_proxy.set("id", idprefix + self.node.get(nodename).get('id'))
        resource_type.set("mimetype", mtype)
        resource_type.text = rtype

        # cut of last part of transcriptfilename for reference
        if self.node.get(nodename).get('type') == 'transcript':
            transnlist = nodename.split('_')
            transnlist.pop()
            transnlist.pop()
            transcriptref = '_'.join(transnlist)

            resource_ref.text = unicode(refprefix + transcriptref + refpostfix)
        elif self.node.get(nodename).get('type') == 'corpus':
            # refer to the original label of the corpus:
            # corpusref = self.node.get(nodename).get('filename').split('-')[0].split('_extern')[0]
            # corrected link to AGD corpus
            corpusref = self.node.get(nodename).get('filename').split('_extern')[0]
            resource_ref.text = unicode(refprefix + corpusref + refpostfix)
        else:
            resource_ref.text = unicode(refprefix + nodename + refpostfix)


    def build_resourceproxy(self):
        """
        inplace resourceproxy generation of the resource.
        modifies the stored etree object of each resource.
        :param :
        :return:
        """

        for resource in self.nodes_iter():

            # pass the node name to define_resourceproxy
            if self.node.get(resource).get("etreeobject") \
                    is not False and resource != 'AGD_root':
                self.define_resourceproxy(resource)

    def define_parts(self, resource):
        """
        define Parts for a given node inside a Relation Element.
        all outgoing edges refer to hasParts relations.
        all ingoing edges refer to isPartOf relations.
        :param resource:
        :return:
        """

        cmdiroot = None
        try:
            # retrieve the etree object of the current node
            cmdi_etrobj = self.node.get(resource).get("etreeobject")
        except AttributeError:
            logging.error("referenced resource node has no attribute 'etreeobject'")
            return

        # set root for accessing the etree object:

        # a) if the type of the current node is "event" or
        if self.node.get(resource).get('type') == 'event':
            try:
                cmdiroot = cmdi_etrobj.xpath('//DGDEvent')[0]
            except:
                logging.error('cannot access DGDEvent as root: ' + resource)
                return

        # b) if the type of the current node is "corpus"
        if self.node.get(resource).get('type') == 'corpus':
            try:
                cmdiroot = cmdi_etrobj.xpath('//DGDCorpus')[0]

                # Set the <SelfLink> element of the object
                selflink = cmdiroot.xpath('//SelfLink')[0]
                selflink.text = str(SVNROOT) + str(self.node.get(resource).get('corpus')) + '/' + str(resource) + '.cmdi'

            except:
                logging.error('cannot access DGDCorpus as root: ' + resource)
                return




        # find all in/out edges for the current node
        in_nodes = [i[0] for i in self.in_edges(resource)]
        out_nodes = [i[1] for i in self.out_edges(resource)]

        # hasPart Elements for out_nodes
        # isPartOf Elements for in_nodes

        # remove speaker references in outward nodes
        for speaker in out_nodes:
            if self.node.get(speaker).get('type') == 'speaker':
                out_nodes.remove(speaker)
                logging.info(speaker + " detached from " + resource)

        # remove
        for speaker in in_nodes:
            if self.node.get(speaker).get('type') == 'speaker':
                in_nodes.remove(speaker)
                logging.info(speaker + " detached from " + resource)

        # remove the abstract node from the resource lists
        if 'AGD_root' in in_nodes:
            in_nodes.remove('AGD_root')
        # remove the self-reference from the resource lists
        if resource in in_nodes:
            in_nodes.remove(resource)

        # make sure there are just unique references
        in_nodes = set(in_nodes)
        out_nodes = set(out_nodes)

        # define the hasPart Elements
        # define a Relation Element as parent for hasPart elements
        if cmdiroot is not None:
            relations = etree.SubElement(cmdiroot, 'dc-inter-relations')
        # find them in
            for node in out_nodes:
                try:
                    if mimetypes.guess_type(self.node.get(node).get('filename'))[0] == 'audio/x-wav':
                        # refer to audio as hasPart
                        source = etree.SubElement(relations, 'hasPart')
                        source.set('href', LANDINGPG + node)
                        source.text = self.node.get(node).get('type').capitalize() + ': ' + node
                    # elif mimetypes.guess_type(self.node.get(node).get('filename'))[0] == 'application/x-cmdi+xml':
                    #     source = etree.SubElement(relations, 'hasPart')
                    #     source.set('href', SVNROOT + node)
                    #     source.text = self.node.get(node).get('type').capitalize() + ': ' + node
                    elif self.node.get(node).get('type') == 'event':
                        # refer to original dgd metadata as source (via landing page)
                        haspart = etree.SubElement(relations, 'hasPart')
                        haspart.set('href', SVNROOT + self.node.get(node).get('corpus')+ '/' + node + '.cmdi')
                        haspart.text = self.node.get(node).get('type').capitalize() + ': ' + node
                    elif self.node.get(node).get('type') == 'transcript':
                        haspart = etree.SubElement(relations, 'hasPart')
                        transnlist = node.split('_')
                        transnlist.pop()
                        transnlist.pop()
                        transcriptref = '_'.join(transnlist)
                        haspart.set('href', LANDINGPG + transcriptref)
                        haspart.text = self.node.get(node).get('type').capitalize() + ': ' + node
                except TypeError:
                    logging.error("check data integrity of outbound node " + node)
                    return
            for node in in_nodes:
                try:
                    ispartof = etree.SubElement(relations, 'isPartOf')
                    ispartof.set('href', SVNROOT + self.node.get(node).get('corpus')+ '/' + node + '.cmdi')
                    ispartof.text = self.node.get(node).get('type').capitalize() + ': ' + node
                except TypeError:
                    logging.error("check data integrity of inbound  node " + node)

            # define a node that refers to the version of this metadata
            isversionof = etree.SubElement(relations, 'isVersionOf')
            isversionof.set('href', SVNROOT + self.node.get(resource).get('corpus') + '/' + resource + '.cmdi')
            isversionof.text = 'Version 0'
            # finally define an "source" element that refers to the original agd metadata
            agd_source = etree.SubElement(relations, 'source')

            # FIXME: <source> stays empty for corpus catalogue metadata
            if self.node.get(resource).get('type') == 'corpus':
                try:
                    agd_source.set('href', LANDINGPG +
                                   self.node.get(resource).get('filename').split('_')[0])
                except TypeError:
                    print "Type Error: " + str(resource)
                    print str(self.node.get(resource).get('filename'))

            else:
                agd_source.set('href', LANDINGPG + resource)
            agd_source.text = 'AGD: ' + resource

    def build_parts(self):
        """
        build the hasPart Relations for all Nodes
        :return:
        """
        for resource in self.nodes_iter():

            # pass the node name to define_resourceproxy
            if self.node.get(resource).get('type') == 'event':
                self.define_parts(resource)

    def check_cmdi_xsd(self, nodename):
        """
        checks if the cmdi record file of a node is valid
        :param nodename:
        :return:
        """
        # optain the current schema of both cmdi profiles
        event_s = etree.XMLSchema(etree.parse('../../data/DGDEvent.xsd'))
        corpus_s = etree.XMLSchema(etree.parse('../../data/DGDCorpus.xsd'))
        if self.node.get(nodename).get('type') == 'corpus':
            return corpus_s.validate(self.node.get(nodename).get('etreeobject'))
        elif self.node.get(nodename).get('type') == 'event':
            return event_s.validate(self.node.get(nodename).get('etreeobject'))
        else:
            return False

    def validate_corpus(self, corpusnode):
        """
        takes a node of a corpus (e.g. 'PF') and checks if it and
        all its successors are valid according to the cmdi profile.
        Online access to profiles not yet implemented.
        :param corpusnode:
        :return: errorlist if exception
        """
        errorlist = list
        if not self.check_cmdi_xsd(corpusnode):

            errorlist.append(corpusnode)
        for subnode in self.successors_iter(corpusnode):
            if self.node.get(subnode).get('type') == 'event':
                if not self.check_cmdi_xsd(subnode):
                    errorlist.append(subnode)

        if len(errorlist) > 0:
            print "there where errors:"
            return errorlist
        else:
            return True



    def _write_cmdi(self, nodename, fname):
        """
        write the cmid-xml of a node to a specified file.
        :param nodename, fname:
        :return:
        """
        self.node.get(nodename).get('etreeobject').write(fname, encoding='utf-8', method='xml',
                                                         xml_declaration="<?xml version='1.0' encoding='UTF-8'?>",
                                                         inclusive_ns_prefixes=['xsi', 'cmd'])

    def write2cmdi(self, corpus, outpath):

        if not os.path.isdir(os.path.abspath(os.path.join(outpath, corpus))):
            os.mkdir(os.path.abspath(os.path.join(outpath, corpus)))

        outpathfinal = os.path.abspath(os.path.join(outpath, corpus))

        for nodename, ndata in self.nodes_iter(data=True):
            if ndata.get('type') == 'event' and ndata.get('corpus') == corpus:
                cmdiheader.define_header(nodename, self)
                self._write_cmdi(nodename, os.path.join(outpathfinal, nodename + '.cmdi'))
            elif ndata.get('type') == 'corpus' and ndata.get('corpus') == corpus:
                cmdiheader.define_header(nodename, self)
                self._write_cmdi(nodename, os.path.join(outpathfinal, nodename + '.cmdi'))


class CorpusIterator(object):
    """
    Iterator is initialized with a corpus path.
    either returns files or, in case of event and speaker,
    the corpus label directories
    """

    def __init__(self, resourcepath, resourcetype, validation=False):
        self.resourcepath = os.path.abspath(resourcepath)
        self.resourcetype = resourcetype
        self._files_iter = iter(os.listdir(self.resourcepath))
        self.validation = validation

    def __iter__(self):
        return self

    def next(self):
        file_name = self._files_iter.next()

        if self.validation:
            res_etree = etree.parse(os.path.join(self.resourcepath, file_name))
            remote_schema = etree.XMLSchema(file=res_etree.getroot().items()[1][1].split(' ')[1])
            isvalid = remote_schema.validate(res_etree)
            return os.path.join(self.resourcepath, file_name), isvalid

        return os.path.join(self.resourcepath, file_name)