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
        self.__notfiled = {'nicht dokumentiert': 'not filed'}
        self.__nonvalue = {'nicht vorhanden': 'none'}

    def replace_nonvalues(self, filename):
        """
        takes a filename or foldername and
        replaces all german generic text nonvalue-strings with more
        international
        ones
        :param filename: string
        :return:
        """

        if os.path.isfile(filename):
            self.__rplace_nv(etree.parse(filename), filename)
        else:
            flist = os.listdir(filename)
            for fn in flist:
                self.__rplace_nv(etree.parse(fn), fn)

    def __rplace_nv(self, etreeobj, filename):
        """

        :param file:
        :return:
        """

        for element in etreeobj.getroot().iter():
            if element.text.lower() in self.__nonvalue:
                element.text = self.__nonvalue.get(element.text.lower())
            if element.text.lower() in self.__notfiled:
                element.text = self.__notfiled.get(element.text.lower())

        fobject = codecs.open(filename, mode='w', encoding='utf-8', )
        etreeobj.write(fobject, method='XML', pretty_print=True,
                       encoding='utf-8')

        fobject.close()
