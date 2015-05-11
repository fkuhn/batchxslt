
__author__ = 'kuhn'

import logging
import os
from lxml import etree
import mimetypes



class cmdiHeader(object):

    def __init__(self):


    def set_header(self, cmdifile):
        """
        set values for all elements in the header of a cmdi file
            <Header>
            <MdCreator>gewiss-coma2cmdi.xsl (Daniel Jettka, CLARIN-GeWiss-KP)</MdCreator>
            <MdCreationDate>2014-02-13</MdCreationDate>
            <MdSelfLink>http://hdl.handle.net/10932/00-01FB-53D5-A740-D401-9</MdSelfLink>
            <MdProfile>clarin.eu:cr1:p_1361876010680</MdProfile>
            <MdCollectionDisplayName>Institut fuer Deutsche Sprache,
            CLARIN-D Zentrum, Mannheim</MdCollectionDisplayName>
        </Header>
        :param cmdifile:
        :return:
        """
        cmdi_etree = etree.parse(cmdifile)
