## About
This python package batch processes "Database for Spoken German"-specific xslt
stylesheets to transform the original dgd metadata to cmdi metadata.

## Installation

 Use ```python setupy.py install ``` to install the package.

## Usage

**April 2015** Notebooks are now updated and can be used for complete orchestration
**Note Feb 2015** For a more up-to-date How-to refer to notebooks/ **   


### Configuration File
All important paths are set in the local config.xml.
<CONFIG> is root element to the
following subelements:
<GLOBAL>, defining global resources like the XSLT processor.
<CORPUS>, which defines parameters for corpus-metadata
<EVENT>, which defines parameters for event-metadata of a corpus
<SPEAKER>, which defines paramters for speaker-metadata of a corpus

Each element uses the attributes "type" and "corpus"
*	"type" defines the type of resource that is refered to in the element
	each  metadata-specific element uses the type values "stylesheet", "indirectory", "prefix", "outdirectory" to
	define the type of reference denoted via the metadata-element.
*	"corpus" defines the alias of the corpus refered to. The alias is the official one of the archive of spoken german.
	(e.g. "AD", "BB", "FOLK" etc.)

### Starting Transformation
Once all parameters are set, call the python script dgdstart.py with the Configuration
file parameter e.g. data/config.xml

### Adding Resources
Resource Proxies, part-of relations and header information to finalize all
cmdi files are added in scripts/add_resources_allcorp.py



### Referenced CMDI Profiles

#### Corpora
http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751614

#### Events
http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751615

Speakers do not use a seperate profile. Every relevant information is extracted from the original
dgd data and inserted into the matching event cmdi files.
