__author__ = 'kuhn'

import os


from batchxslt import cmdiresource
from batchxslt import cmdiheader

corpus = "../cmdiOutput/corpus/"
event = "../cmdiOutput/event/"
speakers = "../cmdiOutput/speakers/"
transcripts = "/home/kuhn/IDS/Repos/svn/dgd2_data_rev1233/dgd2_data"

cmdi_final = '../cmdiPF/'

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

print "resource tree built"

# give ids to nodes
counter = 0
for node in resourcetree.nodes_iter():
    corpuslabel = node.split('_')[0]
    resourcetree.node.get(node).update({'id': corpuslabel + '_' + str(counter)})
    counter += 1
resourcetree.build_resourceproxy()
print "resource proxies written to node contents"


for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.define_parts(nodename)
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.define_parts(nodename)

print "has part relations written to node contents"

for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'speaker':
        resourcetree.speaker2event(nodename)
print "speaker information integrated to event nodes"

for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'event':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))

    elif ndata.get('type') == 'corpus':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))

print "corpus and events written to file"
