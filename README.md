# DGD2CMDI
[![Build Status](https://travis-ci.org/fkuhn/dgd2cmdi.svg?branch=master)](https://travis-ci.org/fkuhn/dgd2cmdi)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/48015f7b8a3a413599785a9d4f134540/badge.svg)](https://www.quantifiedcode.com/app/project/48015f7b8a3a413599785a9d4f134540)[![Documentation Status](https://readthedocs.org/projects/dgd2cmdi/badge/?version=latest)](http://dgd2cmdi.readthedocs.io/en/latest/?badge=latest) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## About
Processing Metadata for the Archive of Spoken German.

## Folder structure

### config/
Contains an example resource configuration file.
### doc/
Contains apidoc and further documentation
### src/
Contains the package's sources
### tests/
Contains some simple tests for travis and pytest

## Installation and Setup

 1. Use ```python setupy.py install ``` to install the package.
 
 2. You will also need an XSLT processor (e.g. SAXON-HE):
 
 `ẁget https://sourceforge.net/projects/saxon/files/Saxon-HE/9.7/SaxonHE9-7-0-8J.zip`
 
 `unzip -d saxon SaxonHE9-7-0-8J.zip`
  
 3. The XSLT stylesheets must be present and referable
 
 4. Create a file in .yml for resource reference, e.g. called "resources.yml".
    An example file can be found in config/. 
 
 5. Define your resources to be processed by using the layout in t  

## Usage

dgd2cmdi installs as a cli command and can be run from the shell.
It requires a configuration file to be passed as first argument.
 




