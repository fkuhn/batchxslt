#!/usr/bin/python
"""
This module contains methods to read in a resource
configuration file.

The configuration file is written in yaml and has the following
form:



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
    corpora = resources.get('corpora')

    print "Stylesheet paths:\n"
    print "Corpus: {}".format(xslt['corpus'])
    print "Event: {}".format(xslt['event'])
    print "Speaker: {}\n".format(xslt['speaker'])
    print "XSLT processor path: {}".format(xslt['processor'])


def call_saxon(resourcetype, resources):
    """
<<<<<<< HEAD
    Calls a xslt processor.
    :param: ds
    :return:
=======
    calls a xslt processor by using the informations
    from the resource configuration file.
>>>>>>> 3bd04a0bfc1917243b211a7331e91b2c1aecb9e0
    """
    xslt = xslt = resources.get('xslt')

    metafilepath = os.path.abspath(resources.meta)
    processor = os.path.abspath(resources.processor)

    # now iterate over each corpus and collect the
    # resource paths
    for corpus in resources.corpus:


        if resourcetype == 'corpus':
            stylesheetpath = os.path.abspath(xslt['corpus'])
            outputpath = os.path.abspath(OUTPATHDIC.get('C'))
            os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                processor, metafilepath,
                stylesheetpath, os.path.join(outputpath,
                                            os.path.basename(metafilepath).split('.')[0]+'.cmdi')))
        elif resourcetype == 'event':

            stylesheetpath = os.path.abspath(stylesheetdic.get('E_XSL'))
            outputpath = os.path.abspath(os.path.join(OUTPATHDIC.get('E'), os.path.basename(metafilepath)))
            for resource in os.listdir(metafilepath):
                os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                    processor, os.path.join(metafilepath,resource),
                    stylesheetpath, os.path.join(outputpath,
                                                '.'.join([resource.split('.')[0],'cmdi']))))

        elif resourcetype == 'speaker':

            stylesheetpath = os.path.abspath(stylesheetdic.get('S_XSL'))
            outputpath = os.path.abspath(os.path.join(OUTPATHDIC.get('S'), os.path.basename(metafilepath)))
            for resource in os.listdir(metafilepath):
                os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                    processor, os.path.join(metafilepath, resource),
                    stylesheetpath, os.path.join(outputpath,
                                                '.'.join([resource.split('.')[0],'cmdi']))))
        else:
            raise ValueError()