__author__ = 'kuhn'

import os


from batchxslt import cmdiresource
from batchxslt import cmdiheader

corpus = "/tmp/cmdi/corpus/"
event = "/tmp/cmdi/events/"
speakers = "/tmp/cmdi/speakers/"
transcripts = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/transcripts/"

cmdi_final = '/tmp/cmdi/cmdiFOLK/'

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

# give ids to nodes
counter = 0
for node in resourcetree.nodes_iter():
    corpuslabel = node.split('_')[0]
    resourcetree.node.get(node).update({'id': corpuslabel + '_' + str(counter)})
    counter += 1

resourcetree.build_resourceproxy()

for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.define_parts(nodename)
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.define_parts(nodename)

for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'speaker':
        resourcetree.speaker2event(nodename)

for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'event':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
    elif ndata.get('type') == 'corpus':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
