# DGD2CMDI
[![Build Status](https://travis-ci.org/fkuhn/dgd2cmdi.svg?branch=master)](https://travis-ci.org/fkuhn/dgd2cmdi)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/48015f7b8a3a413599785a9d4f134540/badge.svg)](https://www.quantifiedcode.com/app/project/48015f7b8a3a413599785a9d4f134540)[![Documentation Status](https://readthedocs.org/projects/dgd2cmdi/badge/?version=latest)](http://dgd2cmdi.readthedocs.io/en/latest/?badge=latest) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## About
Processing Metadata for the Archive of Spoken German.

## Folder structure

### config/
Contains an example resource configuration file.
### doc/
Contains apidoc and further documentation.
### saxon/
The xsl processor
### src/
Contains the package's sources.
### tests/
Contains some simple tests for travis and pytest.
### xslt/
The stylesheets used for data conversion.

## Installation and Setup

 1. Use ```python setup.py install ``` to install the package.
 
 2. You will also need an XSLT processor (e.g. SAXON-HE):
 
 `ẁget https://sourceforge.net/projects/saxon/files/Saxon-HE/9.7/SaxonHE9-7-0-8J.zip`
 
 `unzip -d saxon SaxonHE9-7-0-8J.zip`
  
 3. The XSLT stylesheets must be present and referable.
 
 4. Create a file in .yml for resource reference, e.g. called "resources.yml".
    An example file can be found in config/. 
 
 5. Define your resources to be processed by using the yml layout as shown in
    the sample resource file in samples/

## Usage

dgd2cmdi installs as a cli command ```dgd2cmdi``` and can be run from the shell.
It requires a configuration file (see setup) to be passed as first argument.
For example:
```dgd2cmdi resources_configuration_.yml```
The program parses all resources, first stores them as intermediate
representation and in a final step adds dependencies. You can define where the
files are written by altering the configuration file. Default path for
the intermediate format is /tmp/intermediate_cmdi

## Configuration File Layout
There is a default configuration file named ```resources.yml``` located in the main directory.
The configuration file follows the yml format and is structured as follows:

```

# xslt processor and stylesheet path declaration
processor: "saxon/saxon.jar"
# add the path to the xsl stylesheets
stylesheets:
    corpus: "path/to/corpus.xsl"
    event: "path/to/event.xsl"
    speaker: "path/to/speaker.xsl"

# output paths declarations
output-inter: "path/to/intermediate/transformation/output"
output-final: "path/to/finalized/output"

# resource collection declaration
collection:
    PF:
        corpus: "path/to/corpus/catalogue/file/corpus.xml" # the catalogue file
        event: "path/to/events/"  # the directory containing all of the corpus' events
        speaker: "path/to/speakers" # the directory containing all of the corpus' speakers

# add more corpora here following the convention:
# CORPUSLABEL:
        corpus:
        event:
        speaker:
```






