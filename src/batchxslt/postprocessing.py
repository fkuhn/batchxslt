__author__ = 'kuhn'

import os
import sys
import codecs
from lxml import etree


class PostProcessor(object):
    """
    post processing tasks for each metafile type
    """

    def __init__(self):
        """

        :return:
        """
        # non value processing: define mappings
        self.__notfiled = {'nicht dokumentiert': 'not filed',
                           'Nicht dokumentiert': 'not filed',
                           'Nicht relevant': 'not filed'}
        self.__nonvalue = {'nicht vorhanden': 'none',
                           'Nicht vorhanden': 'none'}
        self.__outputpath = '/home/kuhn/Data/IDS/cmditest'

    def replace_nonvalues(self, filename):
        """
        takes a filename or foldername and
        replaces all german generic text nonvalue-strings with more
        international ones.
        :param filename: string
        :return:
        """

        if os.path.isfile(filename):
            fobj = codecs.open(filename)
            self.__rplace_nv(etree.parse(fobj), filename)
        else:
            flist = os.listdir(filename)
            for fname in flist:
                fobj = codecs.open(filename + '/' + fname)
                self.__rplace_nv(etree.parse(fobj), fname)

    def __rplace_nv(self, etreeobj, fname):
        """

        :param etreeobj, fname:
        :return:
        """

        for element in etreeobj.getroot().iter():
            if element.text is not None:
                if element.text.lower() in self.__nonvalue:
                    element.text = self.__nonvalue.get(element.text.lower())
                if element.text.lower() in self.__notfiled:
                    element.text = self.__notfiled.get(element.text.lower())

        fobject = codecs.open(self.__outputpath + '/' + fname,
                              mode='w+')
        fstring = etree.tostring(etreeobj, method='XML', pretty_print=True,
                                 encoding='utf-8')
        fobject.write(fstring)
        fobject.close()

