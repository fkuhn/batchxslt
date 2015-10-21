import click


@click.command()
@click.option('--single', '-s', )
def transform(dgdmetafile, corpusname, resourcetype):
    """

    :param dgdmetafile:
    :param corpusname:
    :param resourcetype:
    :return:
    """


# make the module name a main function for cli call
if __name__ == '__main__':
    """
    batchxslt processes via command line interface
    :return:
    """
    transform()
