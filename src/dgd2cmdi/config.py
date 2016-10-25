import yaml


def load_configuration(conffile):
    """
    loads a configuration file using yaml format
    :param conffile:
    :return:
    """
    configuration = yaml.load(open(conffile))

    return configuration


class Configuration:

    def __init__(self, ymlobject):
        """
        resource taking information from yaml file.
        :param name: string of resource name (e.g. FOLK)
        :param description: string describing the adressed resource.
        :param pathpatternlist: a list of absolute unix style path-patterns
         refering to all locations where files of the given resource are
         found. the pathpatternlist is used to create a collection of
         ChksResource iterators
        :return:
        """
        self.resources = dict()
        self.adresses = ymlobject.get('adresses')
        for resource in ymlobject.get('resource'):
            self.resources.update({resource.get('resource'): resource})