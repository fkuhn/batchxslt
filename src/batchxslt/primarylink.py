__author__ = 'kuhn'
__doc__ = 'link the cmdi resources by writing resource proxy elements and href attributes'

from collections import OrderedDict
from lxml import etree
import logging
import numpy
import os


class PrimaryDataPath(dict):
    """

    """
    def __init__(self, csvfile):
        super(PrimaryDataPath, self).__init__()
        key_value = numpy.loadtxt(csvfile, dtype='string', delimiter=";")
        self.update({k: v for k, v in key_value})


class TranscriptLinker(OrderedDict):
    """
    Resource Linker takes a path that acts as root and writes their
    associated Transcript file paths to orresponding href
    element attributes.
    """
    def __init__(self, transcriptroot):
        super(TranscriptLinker, self).__init__()

        self.transcriptroot = transcriptroot
        self.corpusnames = os.listdir(self.transcriptroot)

        for corpusname in self.corpusnames:
            # TODO: dict of corpusnames to dict of transcriptnames to href-paths
            self.update({corpusname: self.get_transscripts(corpusname)})
            pass

    def get_transscripts(self, corpusname):
        """
        :param a corpus abbreviation string.
        :return a dict of filename to href-paths
        """
        transcripts = os.listdir(self.transcriptroot+'/'+corpusname)
        transcriptnames = dict()
        for transcript in transcripts:
            transcriptnames.update({transcript:
                                    self.transcriptroot+'/'+corpusname+'/'+transcript})
        return transcriptnames

class AudioLinker(object):
    """
    Audio Linker takes a path that acts as root and writes
    a valid href to their associated metadata.
    """


class VideoLinker(object):
    """
    Media Linker takes a path that acts as root and writes
    their associated metadata.
    """
    def __init__(self, mediaroot):

        self.mediaroot = mediaroot




