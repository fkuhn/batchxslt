from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.4'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'lxml', 'networkx'
    ]

setup(name='dgd2cmdi',
    version=version,
    description="XSLT transformation for cmdi resources of the AGD",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='xslt python xml',
    author='Florian Kuhn',
    author_email='kuhn@ids-mannheim.de',
    url='www.ids-mannheim.de',
    license='Apache v2',
    package_data={'config': ['/config/config.yml'], 'data': ['../data/*']},
    include_package_data= True,
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['dgd2cmdi = dgd2cmdi.dgd2cmdi:main',
             'dgd_trans = dgd2cmdi.dgd2cmdi_trans:main']
    }
)
