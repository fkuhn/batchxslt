__author__ = 'kuhn'

from batchxslt import processor
from batchxslt import cmdiresource
import codecs
import os

dgd_corpus = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/corpora/extern"
dgd_events = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/events/extern"
dgd_speakers = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/speakers/extern"

xsl_corpus = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdCorpus2cmdi.xsl"
xsl_events = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdEvent2cmdi.xsl"
xsl_speakers = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdSpeaker2cmdi.xsl"


pf_corpus = os.path.join(dgd_corpus, 'PF--_extern.xml')
pf_events = os.path.join(dgd_events, 'PF')
pf_speakers = os.path.join(dgd_speakers, 'PF')



