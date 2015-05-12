__author__ = 'kuhn'

import os


from batchxslt import cmdiresource
from batchxslt import cmdiheader

corpus = "/tmp/cmdi/corpus/ZW/"
event = "/tmp/cmdi/events/"
speakers = "//tmp/cmdi/speakers/"
transcripts = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/transcripts/"

cmdi_final = '/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdi/ZW/'

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

resourcetree.build_resourceproxy()

for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.define_parts(nodename)
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.define_parts(nodename)

for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'speaker':
        resourcetree.speaker2event(nodename)

for nodename in resourcetree.nodes_iter():


    if resourcetree.node.get(nodename).get('type') == 'event':

        cmdiheader.define_header(nodename, resourcetree)

        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
    elif resourcetree.node.get(nodename).get('type') == 'corpus':

        cmdiheader.define_header(nodename, resourcetree)

        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))