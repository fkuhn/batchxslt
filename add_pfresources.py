__author__ = 'kuhn'

import os


from batchxslt import cmdiresource

corpus = "/tmp/cmdi/PF/corpus/"
event = "/tmp/cmdi/PF/events/"
speakers = "//tmp/cmdi/PF/speakers/"
transcripts = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/transcripts/"

cmdi_final = '/tmp/cmdi/cmdiPF/'

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

resourcetree.build_resourceproxy()

for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.define_parts(nodename)
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.define_parts(nodename)

for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.speaker2event(nodename)

# FIXME: build_parts is not working


for nodename in resourcetree.nodes_iter():

    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))