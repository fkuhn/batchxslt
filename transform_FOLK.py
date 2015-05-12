__author__ = 'kuhn'

from batchxslt import processor
from batchxslt import cmdiresource
import codecs
import os

dgd_corpus = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/corpora/extern"
dgd_events = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/events/extern"
dgd_speakers = "/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/speakers/extern"

corpus_xsl = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdCorpus2cmdi.xsl"
event_xsl = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdEvent2cmdi.xsl"
speaker_xsl = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/xslt/dgdSpeaker2cmdi.xsl"

saxon_jar = "/home/kuhn/Data/IDS/svn/dgd2_data/dgd2cmdi/batchxslt/saxon/saxon9he.jar"

pf_corpus = os.path.join(dgd_corpus, 'FOLK_extern.xml')
pf_events = os.path.join(dgd_events, 'FOLK')
pf_speakers = os.path.join(dgd_speakers, 'FOLK')

xsl_processor = processor.XSLBatchProcessor(saxon_jar)

xsl_processor.transform(corpus_xsl, pf_corpus, "cmdi_", '/tmp/cmdi/corpus/FOLK/')

xsl_processor.transform(event_xsl, pf_events, "cmdi_", '/tmp/cmdi/events/FOLK/')

xsl_processor.transform(speaker_xsl, pf_speakers, "cmdi_", '/tmp/cmdi/speakers/FOLK/')
