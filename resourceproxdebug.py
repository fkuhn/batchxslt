# test env for debugging of resource proxy generation

# from pudb import set_trace
from batchxslt import cmdiresource

# set_trace()
corpus = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/corpus/"
event = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/event/"
speakers = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/cmdiOutBeta2/speakers/"

resourcetree = cmdiresource.ResourceTreeCollection(corpus, event, speakers)

resourcetree.build_resourceproxy()






