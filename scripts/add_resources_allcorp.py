#!usr/bin/python

import os

from batchxslt import cmdiheader, cmdiresource

# set hardcoded paths for intermediate resources and
# output directory for finalized cmdi files
corpus = "/opt/cmdiOutput/corpus/"
event = "/opt/cmdiOutput/event/"
speakers = "/opt/cmdiOutput/speakers/"
transcripts = "/home/kuhn/IDS/Repos/svn/dgd2_data_rev1233/dgd2_data/transcripts"

cmdi_final = '/tmp/cmdi_finalized/'

def make_directory(pathname):
    try:
        os.mkdir(os.path.abspath(pathname))
    except OSError:
        print "cannot create directory " + pathname
        print "Maybe it already exists..."

# instantiate a resource tree
resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

# iterate over all resource nodes and assign a id label
counter = 0
for node in resourcetree.nodes_iter():
    corpuslabel = node.split('_')[0]
    resourcetree.node.get(node).update({'id': corpuslabel + '_' + str(counter)})
    counter += 1

# generate resource proxy dependencies
resourcetree.build_resourceproxy()

# iterate over all nodes. if their type is 'event' or 'corpus', define their
# part relation elements and dependencies
for nodename in resourcetree.nodes_iter():
    if resourcetree.node.get(nodename).get('type') == 'event':
        resourcetree.define_parts(nodename)
    elif resourcetree.node.get(nodename).get('type') == 'corpus':
        resourcetree.define_parts(nodename)

# iterate over all nodes. if a node's type is 'speaker', insert all
# its relevant information into the corresponding event node
for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'speaker':
        resourcetree.speaker2event(nodename)

# finalize the cmdi files:
# to each 'corpus' and 'event' node, add a corresponding header
# write each node content to a cmdi file
for nodename, ndata in resourcetree.nodes_iter(data=True):
    if ndata.get('type') == 'event':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
    elif ndata.get('type') == 'corpus':
        cmdiheader.define_header(nodename, resourcetree)
        resourcetree.write_cmdi(nodename, os.path.join(cmdi_final, nodename + '.cmdi'))
