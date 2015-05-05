__author__ = 'kuhn'
__doc__ = 'Resource Parser and XLST Processor class definitions.'

import os
import sys
import csv
from lxml import etree


class Configurator(object):
    """
    Simple configuration file parser. template for further extensions.
    Parses config.xml in main module directory. How to use config.xml
    see README.md
    """

    def __init__(self, configfile):
        """
        :param configfile
        :return
        """
        self.configfile = etree.parse(configfile)
        self.root = self.configfile.getroot()
        self.configItemsList = dict()
        self.globals = dict()
        self.speaker = dict()
        self.event = dict()
        self.corpus = dict()

        for item in self.root.iter():

            if item.tag == "GLOBAL":
                self.globals.update({item.get("type"): item.text})
            if item.tag == "CORPUS":
                self.corpus.update({item.get("type"): item.text})
            if item.tag == "EVENT":
                self.event.update({item.get("type"): item.text})
            if item.tag == "SPEAKER":
                self.speaker.update({item.get("type"): item.text})


class CsvConfigurator(object):
    """
    a more flexible config parser using just csv files as input.
    """

    def __init__(self, configfile):

        __configreader = csv.DictReader(open(configfile), delimeter=',')
    pass


class XSLBatchProcessor(object):
    """
    wrapper to call an xslt processor.
    """

    def __init__(self, processorpath):
        """
        :param absolute processorpath: e.g. c:\saxonHE\saxon9he.jar
        :return:
        """
        os.path.exists(processorpath)
        self.processorpath = processorpath

    def transform(self, stylesheet, xmldata, prefix, outputdir):
        """
        this method iterates the xslt processor over all files in a given
        directory using a certain stylesheet and writes the output to a
        defined and existing directory. transform dir is a more simple
        alternative to the 'fully automated' but cumbersome start() method.
        :param stylesheet:
        :param xmldata: either directory or file
        :param prefix:
        :param outputdir:
        :return:
        """

        if os.path.isfile(xmldata):

            try:

                output = os.path.join(outputdir, prefix + xmldata.split('/')[-1])

                os.system(
                    "java -jar " + self.processorpath + " -s:" +
                    xmldata + " -xsl:" + stylesheet
                    + " -o:" + output)
            except OSError:
                print "cannot call processor"
                sys.exit()

        elif os.path.isdir(xmldata):

            for filename in os.listdir(xmldata):

                try:

                    output = os.path.join(outputdir, prefix + filename.split('/')[-1])

                    os.system(
                        "java -jar " + self.processorpath + " -s:" +
                        os.path.join(xmldata, filename) + " -xsl:" + stylesheet
                        + " -o:" + output)
                except OSError:
                    print "cannot call processor"
                    sys.exit()

    def start(self, stylesheet, xmldatadirectory, prefix, outputdir):
        """starts the xslt transformation process and checks if
         directories are reachable"""
        try:

            if os.path.exists(stylesheet):
                print "stylesheet: " + stylesheet
            if os.path.exists(os.path.abspath(outputdir)):
                print "outputdir: " + outputdir
            else:
                print "outputdir not readable: " + outputdir
            if os.path.exists(xmldatadirectory):
                print "xmldata: " + xmldatadirectory

            xmldir = os.listdir(xmldatadirectory)

        except OSError():
            print "xml Data directory is not readable"
            sys.exit()

        for metafile in xmldir:

            if os.path.isfile(xmldatadirectory + '/' + metafile) is True:
                output = outputdir + "/" + prefix + metafile
                """
                saxon call parameters:
                -s:source -xsl:stylesheet -o:output
                """
                try:
                    # print "processing " + metafile
                    os.system(
                        "java -jar " + self.processorpath + " -s:" +
                        xmldatadirectory + "/" +
                        metafile + " -xsl:" + stylesheet
                        + " -o:" + output)
                except OSError:
                    print "cannot call processor"
                    sys.exit()

            if os.path.isdir(xmldatadirectory + "/" + metafile) is True:
                # change scope of outputdir
                # os.path.abspath()
                try:
                    os.mkdir(os.path.abspath(outputdir + '/' + metafile))
                except OSError:
                    print "cannot create directory " + outputdir + "/" + metafile
                    print "Maybe it already exists..."

                for singlefile in os.listdir(xmldatadirectory + "/" + metafile):

                    output = os.path.abspath(
                        outputdir + '/' + metafile + "/" + prefix + singlefile)
                    """
                    -s:source -xsl:stylesheet -o:output
                    """

                    try:
                        # call the xslt processor
                        os.system(
                            "java -jar " + self.processorpath
                            + " -s:" + xmldatadirectory + "/" + metafile + "/"
                            + singlefile + " -xsl:"
                            + stylesheet
                            + " -o:" + output)

                    except OSError:
                        print "cannot call processor"
                        sys.exit()
                        # check if item is a directory (single corpus dir)

        return

