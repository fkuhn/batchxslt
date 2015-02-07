## ABOUT
This small python package batch processes "Database for Spoken German"-specific xslt
stylesheets to transform the original dgd metadata to cmdi metadata.


## INSTALLATION

 Use ```python setupy.py install ``` to install the package.


## USAGE

### CONFIGURATION
All important paths are set in the local config.xml. <CONFIG> is root element to the
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

### START
Once all parameters are set, just start the python script  

	
## CHANGELOG

### Version 0.1.1 
* now uses path.abspath to refer to resources

### Version 0.1
* corpus transformation working
* changed configuration paths in config.xml to relative paths
* added saxon processor jarfile to batchxsl/saxon and refer to it in config.xml

### Version 0.1a
* configuration parameter constants found in runCorpus.py.
* Just start runCorpus.py after setting parameters right.
* main.py is a template for configuration settings for the run*.py files at the moment.
