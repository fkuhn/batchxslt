__doc__ = "test env for debugging of resource proxy generation"

# from pudb import set_trace
from batchxslt import cmdiresource

# set_trace()
corpus = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/corpus/"
event = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/event/"
speakers = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/speakers/"
transcripts = "/home/kuhn/Data/IDS/svn/dgd2_data/transcripts/"

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers, transcripts)

resourcetree.build_resourceproxy()

resourcetree.write_cmdi('FOLK', '/tmp/folktest.xml')

# TODO: For corpus labels: every resource must be put into the resource proxy list



