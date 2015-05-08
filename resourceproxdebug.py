__doc__ = "test env for debugging of resource proxy generation"

# from pudb import set_trace
from batchxslt import cmdiresource

# set_trace()


dgd_corpus = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/corpora"
dgd_event = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/events"
dgd_speakers = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/speakers"

cmdi_corpus = "/home/kuhn/Data/IDS/cmdi/corpus"
cmdi_event = "/home/kuhn/Data/IDS/cmdi/event"
cmdi_speakers = "/home/kuhn/Data/IDS/cmdi/speakers"

transcripts = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/transcripts/"

resourcetree = cmdiresource.ResourceTreeCollection(cmdi_corpus, cmdi_event, cmdi_speakers, transcripts)

print "emtpy spawned nodes:"
print len(resourcetree.show_empty_etree())


print resourcetree.node.get('MV')

print resourcetree.node.get('MV').get('etreeobject').getroot()
print resourcetree.node.get('FOLK').get('etreeobject').getroot()

resourcetree.build_resourceproxy()

resourcetree.write_cmdi('PF--_E_00001', '/tmp/pf_event.xml')

# TODO: For corpus labels: every resource must be put into the resource proxy list



