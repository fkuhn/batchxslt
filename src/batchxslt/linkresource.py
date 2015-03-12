__author__ = 'kuhn'
__doc__ = 'link the cmdi resources by writing resource proxy elements and href attributes'

from lxml import etree
import logging


class ResourceLinker(object):
    """
    Resource Linker takes a ResourceTree and writes their
    associated metadata and media files corresponding
    elements.
    """
    def __init__(self, resourcetree):

        logging.info(etree.LIBXML_VERSION)

        self.resourcetree = resourcetree

        # TODO:


        return
