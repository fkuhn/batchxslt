__author__ = 'kuhn'
__doc__ = """<Header>
      <MdCreator>DGD2CMDI</MdCreator>
      <MdCreationDate>2015-05-07+02:00</MdCreationDate>
      <MdSelfLink>file:/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/events/extern/PF/PF--_E_00127_extern.xml</MdSelfLink>
      <MdProfile>clarin.eu:cr1:p_1430905751592</MdProfile>
      <MdCollectionDisplayName>AGD</MdCollectionDisplayName>
        </Header>"""

import logging
import os
from lxml import etree
import mimetypes

MDCREATOR = 'batchxslt.py'
VALIDIDS = {'event': 'clarin.eu:cr1:p_1430905751604', 'corpus': 'clarin.eu:cr1:p_1430905751603'}
SVNROOT = 'dgd2_data/dgd2cmdi/cmdi/PF/'


def define_header(cmdinode, resourcetree):
    """
    sets MdSelfLink and tests if MdProfile ID is valid
    :param cmdinode:
    :return:
    """
    cmdifilename = resourcetree.node.get(cmdinode).get('filename').split('.')[0] + '.cmdi'
    cmdiheader = resourcetree.node.get(cmdinode).get('etreeobject').getroot().find('Header')

    cmdimdselflink = cmdiheader.find('MdSelfLink')
    cmdiprofile = cmdiheader.find('MdProfile')

    if cmdiprofile.text not in VALIDIDS.itervalues():
        logging.error('The profile id of MdProfile is not valid: ' + cmdifilename.split('/')[-1])

    # get the path

    cmdimdselflink.text = SVNROOT + cmdifilename