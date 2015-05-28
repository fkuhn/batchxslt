__author__ = 'kuhn'
__doc__ = """<Header>
      <MdCreator>DGD2CMDI</MdCreator>
      <MdCreationDate>2015-05-07+02:00</MdCreationDate>
      <MdSelfLink>file:/home/kuhn/Data/IDS/svn_rev1233/dgd2_data/metadata/events/extern/PF/PF--_E_00127_extern.xml</MdSelfLink>
      <MdProfile>clarin.eu:cr1:p_1430905751592</MdProfile>
      <MdCollectionDisplayName>AGD</MdCollectionDisplayName>
        </Header>"""

import logging
import requests
from lxml import etree

MDCREATOR = 'batchxslt.py'
VALIDIDS = {'event': 'clarin.eu:cr1:p_1430905751615', 'corpus': 'clarin.eu:cr1:p_1430905751614'}
SVNROOT = 'dgd2_data/dgd2cmdi/cmdi/PF/'
EVENTXSDURI = "http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751615/xsd"
CORPUSXSDURI = "http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751614/xsd"

def check_cmdi_xsd(nodename):
    """
    checks if the cmdi record file of a node is valid
    :param nodename:
    :return:
    """
    # optain the current schema of both cmdi profiles
    event_s = requests.get(EVENTXSDURI)



def define_header(cmdinode, resourcetree, override_profile=False):
    """
    sets MdSelfLink and tests if MdProfile ID is valid
    :param cmdinode:
    :return:
    """

    cmdifilename = cmdinode + '.cmdi'

    cmdiheader = resourcetree.node.get(cmdinode).get('etreeobject').getroot().find('Header')

    cmdiroot = resourcetree.node.get(cmdinode).get('etreeobject').getroot()
    cmdiroot.set('xmlns', 'http://www.clarin.eu/cmd/')

    cmdimdselflink = cmdiheader.find('MdSelfLink')
    cmdiprofile = cmdiheader.find('MdProfile')

    # TODO: profile validation via clarin component registry.
    if cmdiprofile.text not in VALIDIDS.itervalues() and override_profile is False:
        logging.error('The profile id of MdProfile is not valid: ' + cmdifilename.split('/')[-1])

    # get the path

    cmdimdselflink.text = SVNROOT + cmdifilename
