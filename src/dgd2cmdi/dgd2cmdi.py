#!/usr/bin/python
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
    processor = resources['processor']
    xslt = resources.get('stylesheets')
    print "Processorpath: {}".format(processor)
    print "Stylesheet paths:\n"
    print "Corpus: {}".format(xslt['corpus'])
    print "Event: {}".format(xslt['event'])
    print "Speaker: {}".format(xslt['speaker'])
    print resources.get('collection')
    resdic = resources.get('collection')
    for coll in resdic:
        print resdic.get(coll).get('speaker')
        
        # Iterate over the resource and call the processor



# if __name__ == '__main__':
#    main()

# TODO: configuration file processing
# TODO: subcommand for each conversion step
# TODO: 'transform' and 'add_dep'

