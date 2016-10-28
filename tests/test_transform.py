import pytest
import os
from lxml import etree

"""
Test Questions:

Is non-valid xml handled without breaking
the pipeline?
Are missing subelements treated appropriately?
"""

#TDATA = {
#    "corpus": os.path.abspath("testdata/corpus.xml"),
#    "event": os.path.abspath("testdata/event.xml"),
#    "speaker": os.path.abspath("testdata/speaker.xml")
#}


def test_catalogue():
    """
    tests corpus catalogue metadata
    transformation
    :return:
    """
    #xmlparser = etree.XMLParser()
    #tree = etree.parse(TDATA["corpus"], parser=xmlparser)
    #assert tree.getroot() is not None
    pass


def test_event():
    pass


def test_speaker():
    pass

