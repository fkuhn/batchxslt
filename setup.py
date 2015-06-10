from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'lxml', 'networkx', 'numpy'
    ]

setup(name='dgd2cmdi',
    version=version,
    description="batch transformation for xsl stylesheets",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='xslt batch python xml',
    author='Florian Kuhn',
    author_email='kuhn@ids-mannheim.de',
    url='www.ids-mannheim.de',
    license='Apache v2',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['dgd2cmdi=dgd2cmdi:main']
    }
)
