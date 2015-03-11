__author__ = 'kuhn'
__doc__ = 'collection of classes being deprecated'
import networkx
from lxml import etree
import codecs
import logging


class ResourceTree(networkx.DiGraph):
    """
    a b-tree structure to link all local dgd resources, generated for
    each dgd metadata file.
    Starting point: ResourceBTree is a child of networkx.DiGraph
    """

    # TODO: Find a packages for tree representation or use networx

    def __init__(self, filename):
        super(ResourceTree).__init__()
        """
        init a resource tree object as directed graph:
        read in a cmdi-transformed dgd metafile
        :return:
        """
        self.etreeobject = None
        try:
            self.etreeobject = etree.parse(codecs.open(filename,
                                                       encoding="utf-8"))

        except IOError:
            logging.error("file not readable")

        fileroot = self.etreeobject.getroot()

        for element in fileroot.iter():
            print



