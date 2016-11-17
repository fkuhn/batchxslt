#!/usr/bin/python
"""=
This module provides methods to read the configuration file,
process the referenced resources and
"""
import argparse
import codecs
import os

import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    'resources', help='a file containing paths of a resource (corpus, event, speaker) to transform')


def main():
    """
    Main Method for dgd to cmdi transformation
    :return:
    """
    args = parser.parse_args()
    with codecs.open(args.resources, mode='r', encoding='utf-8') as resfile:
        resources = yaml.safe_load(resfile)
    # processor = resources['processor']
    # xslt = resources.get('stylesheets')
    # print "Processorpath: {}".format(processor)
    # print "Stylesheet paths:\n"
    # print "Corpus: {}".format(xslt['corpus'])
    # print "Event: {}".format(xslt['event'])
    # print "Speaker: {}".format(xslt['speaker'])
    # print resources.get('collection')
    # resdic = resources.get('collection')
    # for coll in resdic:
    #    print resdic.get(coll).get('speaker')

        # Iterate over the resource and call the processor
    transform(resources)


def transform(resources):
    """
    calls the processor and refers to all resources
    given in the configuration file.
    """
    # define vars from config file
    processor = resources['processor']
    stylesheets = resources['stylesheets']
    collection = resources['collection']
    outputinter_corpus = resources['output-inter-corpus']
    outputinter_events = resources['output-inter-events']
    outputinter_speakers = resources['output-inter-speakers']
    outputfinal = resources['output-final']

    for resource in collection:

        corpus_inpath = collection.get(resource).get('corpus')
        events_inpath = collection.get(resource).get('event')
        speakers_inpath = collection.get(resource).get('speaker')

        outputfolder_corpus = prepare_cpath(outputinter_corpus, resource)
        outputfolder_event = prepare_cpath(outputinter_events, resource)
        outputfolder_speaker = prepare_cpath(outputinter_speakers, resource)

        call_processor(corpus_inpath, 'corpus', stylesheets,
                       processor, outputfolder_corpus)
        call_processor(events_inpath, 'event', stylesheets,
                       processor, outputfolder_event)
        call_processor(speakers_inpath, 'speaker', stylesheets,
                       processor, outputfolder_speaker)


def call_processor(metafilepath, resourcetype, stylesheetdic, processor, outputpath):
    """
    calls the xslt processor
    """
    metafilepath = os.path.abspath(metafilepath)
    processor = os.path.abspath(processor)

    if resourcetype == 'corpus':
        stylesheetpath = os.path.abspath(stylesheetdic.get('corpus'))
        outputpath = os.path.abspath(outputpath)
        os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
            processor, metafilepath,
            stylesheetpath, os.path.join(outputpath,
                                         os.path.basename(
                                             metafilepath).split('.')[0] + '.cmdi')))
    elif resourcetype == 'event':

        stylesheetpath = os.path.abspath(stylesheetdic.get('event'))
        outputpath = os.path.abspath(os.path.join(
            outputpath, os.path.basename(metafilepath)))
        for resource in os.listdir(metafilepath):
            os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                processor, os.path.join(metafilepath, resource),
                stylesheetpath, os.path.join(outputpath,
                                             '.'.join([resource.split('.')[0], 'cmdi']))))

    elif resourcetype == 'speaker':

        stylesheetpath = os.path.abspath(stylesheetdic.get('speaker'))
        outputpath = os.path.abspath(os.path.join(
            outputpath, os.path.basename(metafilepath)))
        for resource in os.listdir(metafilepath):
            os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
                processor, os.path.join(metafilepath, resource),
                stylesheetpath, os.path.join(outputpath,
                                             '.'.join([resource.split('.')[0], 'cmdi']))))
    else:
        raise ValueError()


def finalize_resources():
    """
    The final step adding resource proxies, cmdi headers and speaker
    informations in event metafiles.
    """
    pass

# -------------------------------
# Some helper methods and classes
# -------------------------------


def prepare_cpath(outfolder, cname):
    """
    creates a valid path to a resource collection
    named after the corpus label.
    """
    if not os.path.isdir(os.path.join(outfolder, cname)):
        os.mkdir(os.path.join(outfolder, cname))

    return os.path.join(outfolder, cname)


class CorpusIterator(object):
    """
    Iterator is initialized with a corpus path.
    either returns files or, in case of event and speaker,
    the corpus label directories
    """

    def __init__(self, resourcepath, resourcetype):
        self.resourcepath = os.path.abspath(resourcepath)
        self.resourcetype = resourcetype
        self._files_iter = iter(os.listdir(self.resourcepath))

    def __iter__(self):
        return self

    def next(self):
        file_name = self._files_iter.next()
        return os.path.join(self.resourcepath, file_name)
