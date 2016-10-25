import pytest
from lxml import etree

"""
Test Questions:

Is non-valid xml handled without breaking
the pipeline?
Are missing subelements treated appropriately?
"""

TDATA = {
    "corpus": "testdata/corpus.xml",
    "event": "testdata/event.xml",
    "speaker": "testdata/speaker.xml"
}


def test_catalogue():
    """
    tests corpus catalogue metadata
    transformation
    :return:
    """
    xmlparser = etree.XMLParser()
    tree = etree.parse(TDATA["corpus"], parser=xmlparser)
    assert tree.getroot() is not None


def test_event():
    pass


def test_speaker():
    pass

