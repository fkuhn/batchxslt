__author__ = 'kuhn'

import os
import sys

from lxml import etree


class ConfigParser:
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


class XSLBatchProcessor:
    """
    a very simple wrapper to call an xsl processor.
    """

    def __init__(self, processorpath):
        """
        :param absolute processorpath: e.g. c:\saxonHE\saxon9he.jar
        :return:
        """
        os.path.exists(processorpath)
        self.processorpath = processorpath


    def start(self, stylesheet, xmldatadirectory, prefix, outputdir):

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
            print xmldir

        except OSError:
            print "xml Data directory is not readable"
            sys.exit()

        for metafile in xmldir:
            # os.chdir(outputdir)

            if os.path.isfile(xmldatadirectory + '/' + metafile) is True:
                output = outputdir + "/" + prefix + metafile
                print output
                """
                -s:source -xsl:stylesheet -o:output
                """
                try:
                    print "processing " + metafile
                    os.system(
                        "java -jar " + self.processorpath + " -s:" + xmldatadirectory + "/" + metafile + " -xsl:" + stylesheet
                        + " -o:" + output)
                except OSError:
                    print "cannot call processor"
                    sys.exit()

            if os.path.isdir(xmldatadirectory + "/" + metafile) is True:
                print metafile
                # change scope of outputdir
                # os.path.abspath()

                # TODO: deal with subdirectory creation for events and speakers

                try:
                    os.mkdir(os.path.abspath(outputdir + '/' + metafile))
                except OSError:
                    print "cannot create directory " + outputdir + "/" + metafile
                    print "Maybe it already exists..."

                for singlefile in os.listdir(xmldatadirectory + "/" + metafile):

                    output = os.path.abspath(outputdir + '/' + metafile + "/" + prefix + singlefile)
                    print output
                    """
                    -s:source -xsl:stylesheet -o:output
                    """

                    try:
                        # call the xslt processor
                        print "processing " + singlefile
                        os.system(
                            "java -jar " + self.processorpath + " -s:" + xmldatadirectory + "/" + metafile + "/"
                            + singlefile + " -xsl:"
                            + stylesheet
                            + " -o:" + output)

                    except OSError:
                        print "cannot call processor"
                        sys.exit()
                        # check if item is a directory (single corpus dir)

        return

