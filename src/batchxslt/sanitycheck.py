import hashlib

__author__ = 'kuhn'
__doc__ = 'check integrity of referenced resources'
# TODO: md5 check
# TODO: accessability check


class SanityChecker(object):

    def __init__(self):
        """

        :return:
        """

    @staticmethod
    def genchecksum(fileobject):
        """
        uses old but sufficient md5 checksum
        :param fileobject:
        :return: chksum
        """
        return hashlib.md5(fileobject).hexdigest()
