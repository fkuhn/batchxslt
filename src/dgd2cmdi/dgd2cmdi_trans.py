#!/usr/bin/python
"""
This module contains methods to read in a resource
configuration file and to
"""
import os
import codecs
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('resources', help='a file containing paths of a resource (corpus, event, speaker) to transform')


def main():
    """
    Main Method for dgd to cmdi transformation
    :return:
    """
    args = parser.parse_args()
    with codecs.open(args.resources, mode='r', encoding='utf-8') as resfile:
        resources = yaml.safe_load(resfile)
    xslt = resources.get('xslt')
    print "Stylesheet paths:\n"
    print "Corpus: {}".format(xslt['corpus'])
    print "Event: {}".format(xslt['event'])
    print "Speaker: {}\n".format(xslt['speaker'])
    print "XSLT processor path: {}".format(xslt['processor'])


def call_saxon(resourcetype, resources):
    """
    calls a xslt processor by using the informations
    from the resource configuration file.
    """
    xslt = xslt = resources.get('xslt')

    metafilepath = os.path.abspath(metafilepath)
    saxonpath = os.path.abspath(saxonpath)

    if resourcetype == 'corpus':
        stylesheetpath = os.path.abspath(xslt['corpus'])
        outputpath = os.path.abspath(OUTPATHDIC.get('C'))
        os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
            saxonpath, metafilepath,
            stylesheetpath, os.path.join(outputpath,
                                         os.path.basename(metafilepath).split('.')[0]+'.cmdi')))
    elif resourcetype == 'event':

        stylesheetpath = os.path.abspath(stylesheetdic.get('E_XSL'))
        outputpath = os.path.abspath(os.path.join(OUTPATHDIC.get('E'), os.path.basename(metafilepath)))
        for resource in os.listdir(metafilepath):
            os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                saxonpath, os.path.join(metafilepath,resource),
                stylesheetpath, os.path.join(outputpath,
                                             '.'.join([resource.split('.')[0],'cmdi']))))

    elif resourcetype == 'speaker':

        stylesheetpath = os.path.abspath(stylesheetdic.get('S_XSL'))
        outputpath = os.path.abspath(os.path.join(OUTPATHDIC.get('S'), os.path.basename(metafilepath)))
        for resource in os.listdir(metafilepath):
            os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                saxonpath, os.path.join(metafilepath, resource),
                stylesheetpath, os.path.join(outputpath,
                                             '.'.join([resource.split('.')[0],'cmdi']))))
    else:
        raise ValueError()