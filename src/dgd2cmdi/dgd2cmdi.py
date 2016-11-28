"""
This module provides methods to read the configuration file,
process the referenced resources and
"""
import argparse
import codecs
import os
import sys
import subprocess


import yaml

import cmdiresource
import cmdiheader
from lxml import etree

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    'resources',
    help='a file containing paths of a resource (corpus, event, speaker) to transform'
)


def main():
    """
    Main Method for dgd to cmdi transformation
    :return:
    """
    args = PARSER.parse_args()
    with codecs.open(args.resources, mode='r', encoding='utf-8') as resfile:
        resources = yaml.safe_load(resfile)

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
    transcripts = resources['transcripts']
    outputinter_corpus = resources['output-inter-corpus']
    outputinter_events = resources['output-inter-events']
    outputinter_speakers = resources['output-inter-speakers']

    outputfinal = resources['output-final']

    for resource in collection:

        corpus_inpath = collection.get(resource).get('corpus')
        events_inpath = collection.get(resource).get('event')
        speakers_inpath = collection.get(resource).get('speaker')

        outputfolder_corpus = outputinter_corpus
        outputfolder_event = prepare_cpath(outputinter_events, resource)
        outputfolder_speaker = prepare_cpath(outputinter_speakers, resource)

        event_iterator = FileIterator(events_inpath, 'event')
        speaker_iterator = FileIterator(speakers_inpath, 'speaker')

        call_processor(corpus_inpath, 'corpus', stylesheets, processor,
                       outputfolder_corpus)

        events = {}
        for event_resourcefile in event_iterator:
            call_processor(event_resourcefile, 'event', stylesheets, processor,
                           outputfolder_event)

        speakers = {}
        for speaker_resourcefile in speaker_iterator:
            call_processor(speaker_resourcefile, 'speaker', stylesheets,
                           processor, outputfolder_speaker)

        # trans_resources.update({resource: (corpus, events, speakers)})

        # return trans_resources
    finalize_resources(outputinter_corpus, outputinter_events,
                       outputinter_speakers, transcripts, outputfinal, collection)


def call_inline_processor(metafilepath, resourcetype, stylesheetdic, processor,
                          outputpath):
    """
    transforms resources inline by using
    subprocess and parsing the returncode
    with etree.
    returns a dictionary with filename key  and etree value 
    """
    metafilepath = os.path.abspath(metafilepath)
    processor = os.path.abspath(processor)
    converts = {}

    if resourcetype == 'corpus':
        stylesheetpath = os.path.abspath(stylesheetdic.get('corpus'))
        outputpath = os.path.abspath(outputpath)
        command = "java -jar {} -s:{} -xsl:{}".format(processor, metafilepath,
                                                      stylesheetpath)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        converts.update({
            os.path.basename(metafilepath): etree.parse(process.stdout)
        })
        return converts

    elif resourcetype == 'event':
        stylesheetpath = os.path.abspath(stylesheetdic.get('event'))
        outputpath = os.path.abspath(outputpath)
        command = "java -jar {} -s:{} -xsl:{}".format(processor, metafilepath,
                                                      stylesheetpath)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        converts.update({
            os.path.basename(metafilepath): etree.parse(process.stdout)
        })
        return converts

    elif resourcetype == 'speaker':
        stylesheetpath = os.path.abspath(stylesheetdic.get('speaker'))
        outputpath = os.path.abspath(outputpath)
        command = "java -jar {} -s:{} -xsl:{}".format(processor, metafilepath,
                                                      stylesheetpath)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        converts.update({
            os.path.basename(metafilepath): etree.parse(process.stdout)
        })
        return converts

    else:
        raise ValueError()


def call_processor(metafilepath, resourcetype, stylesheetdic, processor,
                   outputpath):
    """
    calls the xslt processor for one resource instance.
    """

    metafilepath = os.path.abspath(metafilepath)
    processor = os.path.abspath(processor)

    if resourcetype == 'corpus':
        stylesheetpath = os.path.abspath(stylesheetdic.get('corpus'))
        outputpath = os.path.abspath(outputpath)
        os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
            processor, metafilepath, stylesheetpath,
            os.path.join(outputpath,
                         os.path.basename(metafilepath).split('.')[0] +
                         '.cmdi')))
    
    elif resourcetype == 'event':
        stylesheetpath = os.path.abspath(stylesheetdic.get('event'))

        outputpath = os.path.abspath(outputpath)

        # for resource in os.listdir(metafilepath):
        os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
            processor,
            os.path.join(metafilepath), stylesheetpath,
            os.path.join(outputpath,
                         os.path.basename(metafilepath).split('.')[0] +
                         '.cmdi')))

    elif resourcetype == 'speaker':

        stylesheetpath = os.path.abspath(stylesheetdic.get('speaker'))

        outputpath = os.path.abspath(outputpath)
        #   os.path.join(outputpath, os.path.basename(metafilepath)))

        # for resource in os.listdir(metafilepath):
        os.system("java -jar {} -s:{} -xsl:{} -o:{}".format(
            processor,
            os.path.join(metafilepath), stylesheetpath,
            os.path.join(outputpath,
                         os.path.basename(metafilepath).split('.')[0] +
                         '.cmdi')))
    else:
        raise ValueError()


def finalize_resources(corpus, event, speaker, transcripts, finaldir, clabels):
    """The final step adding resource proxies, cmdi headers and speaker
    informations in event metafiles.
    """
    restree = cmdiresource.ResourceTreeCollection(corpus, event, speaker,
                                                  transcripts)
    counter = 0
    # create ids
    for node in restree.nodes_iter():
        corpuslabel = node.split('_')[0]
        restree.node.get(node).update({'id': corpuslabel + '_' + str(counter)})
        counter += 1

    restree.build_resourceproxy()
    print list(restree.nodes())

    for nodename in restree.nodes_iter():
        if restree.node.get(nodename).get('type') == 'event':
            restree.define_parts(nodename)
        elif restree.node.get(nodename).get('type') == 'corpus':
            restree.define_parts(nodename)

    for nodename, ndata in restree.nodes_iter(data=True):
        if ndata.get('type') == 'speaker':
            restree.speaker2event(nodename)

    for cl in clabels:

        write2cmdi(restree, cl, finaldir)

    for nodename, ndata in restree.nodes_iter(data=True):
        print etree.tostring(ndata.get('etreeobject'))

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


# Print iterations progress
# def print_progress(iteration,
#                    total,
#                    prefix='',
#                    suffix='',
#                    decimals=1,
#                    bar_length=100):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         bar_length  - Optional  : character length of bar (Int)
#     """
#     str_format = "{0:." + str(decimals) + "f}"
#     percents = str_format.format(100 * (iteration / float(total)))
#     filled_length = int(round(bar_length * iteration / float(total)))
#     bar = '*' * filled_length + '-' * (bar_length - filled_length)
#
#     sys.stdout.write('\r%s |%s| %s%s %s' %
#                      (prefix, bar, percents, '%', suffix)),
#
#     if iteration == total:
#         sys.stdout.write('\n')
#     sys.stdout.flush()
#
def write2cmdi(restree, corpus, outpath):

    if not os.path.isdir(os.path.abspath(os.path.join(outpath, corpus))):
        os.mkdir(os.path.join(outpath, corpus))

    outpathfinal = os.path.abspath(os.path.join(outpath, corpus))

    for nodename, ndata in restree.nodes_iter(data=True):
        if ndata.get('type') == 'event' and ndata.get('corpus') == corpus:
            cmdiheader.define_header(nodename, restree)
            restree._write_cmdi(nodename, os.path.join(
                outpathfinal, nodename) + '.cmdi')
        elif ndata.get('type') == 'corpus' and ndata.get('corpus') == corpus:
            cmdiheader.define_header(nodename, restree)
            restree._write_cmdi(nodename, os.path.join(
                outpathfinal, nodename) + '.cmdi')


class FileIterator(object):
    """
    Iterator is initialized with a corpus path.
    either returns files or, in case of event and speaker,
    the corpus label directories
    """

    def __init__(self, resourcepath, resourcetype):
        self.resourcepath = os.path.abspath(resourcepath)
        self.resourcetype = resourcetype
        self._files_iter = iter(os.listdir(self.resourcepath))

# TODO: configuration file processing
# TODO: subcommand for each conversion step
# TODO: 'transform' and 'add_dep'

    def __iter__(self):
        return self

    def next(self):
        """
        next element.
        """
        file_name = self._files_iter.next()
        return os.path.join(self.resourcepath, file_name)
